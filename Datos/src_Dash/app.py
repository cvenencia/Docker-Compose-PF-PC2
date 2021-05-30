import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
import psycopg2
import plotly.express as px
import pandas as pd

conectado = False
while not conectado:
    try:
        conn = psycopg2.connect(
            host="postgres",
            database="covid",
            user="postgres",
            password="12345")
        cursor = conn.cursor()
        conectado = True
    except psycopg2.OperationalError:
        pass

query1 = "select count(*) from datos where nombre_municipio like '%BARRANQUILLA%' and "
query2 = "select count(*) from datos where recuperado like "

hombres = []
mujeres = []
recuperados = []
fallecidos = []
labels = []
edad = 0
sw = True
salto_edad = 10
while sw:
    q_edad = "edad > " + str(edad) + " and edad <= " + str(edad + salto_edad) + " "

    q = query1 + q_edad + "and sexo = 'F'"
    cursor.execute(q)
    cant = cursor.fetchall()[0][0]
    mujeres.append(cant)

    q = query1 + q_edad + "and sexo = 'M'"
    cursor.execute(q)
    cant = cursor.fetchall()[0][0]
    hombres.append(cant)

    q = query2 + "'%Recuperado%' and " + q_edad
    cursor.execute(q)
    cant = cursor.fetchall()[0][0]
    recuperados.append(cant)

    q = query2 + "'%Fallecido%' and " + q_edad
    cursor.execute(q)
    cant = cursor.fetchall()[0][0]
    fallecidos.append(cant)

    labels.append(str(edad) + "-" + str(edad + salto_edad))

    edad += salto_edad
    if edad > 100:
        sw = False

query = "select count(*) from datos where tipo_contagio="

tipos_contagiados = []
q = query + "'Comunitaria'"
cursor.execute(q)
cant = cursor.fetchall()[0][0]
tipos_contagiados.append([cant, 'Comunitaria'])

q = query + "'En estudio'"
cursor.execute(q)
cant = cursor.fetchall()[0][0]
tipos_contagiados.append([cant, 'En estudio'])

q = query + "'Importado'"
cursor.execute(q)
cant = cursor.fetchall()[0][0]
tipos_contagiados.append([cant, 'Importado'])

q = query + "'Relacionado'"
cursor.execute(q)
cant = cursor.fetchall()[0][0]
tipos_contagiados.append([cant, 'Relacionado'])

print(tipos_contagiados)

df = pd.DataFrame(tipos_contagiados, columns=['Cantidad', 'Tipo de contagio'])
print(df)
fig = px.pie(df, values='Cantidad', names='Tipo de contagio', title="Distribución de los tipos de contagio en Colombia")

cursor.close()
conn.close()

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.H1(children='Visualizaciones en Dash'),

        html.Div(children='''
            Covid-19 en Barranquilla y Colombia
        '''),

        dcc.Graph(
            id='graph1',
            figure={
                "data": [
                    {"x": labels, "y": hombres, "type": "bar", "name": "Hombres"},
                    {
                        "x": labels,
                        "y": mujeres,
                        "type": "bar",
                        "name": "Mujeres",
                    },
                ],
                "layout": {"title": "Cantidad de contagiados en Barranquilla por edad y sexo"}
            },
        ),
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        dcc.Graph(
            id='graph2',
            figure={
                "data": [
                    {"x": labels, "y": recuperados, "type": "bar", "name": "Recuperados"},
                    {
                        "x": labels,
                        "y": fallecidos,
                        "type": "bar",
                        "name": "Fallecidos",
                    },
                ],
                "layout": {"title": "Cantidad de recuperados y fallecidos en Colombia por edad"}
            },
        ),
    ]),
    html.Div([
        dcc.Graph(
            id='graph3',
            figure=fig
        ),
    ]),
])

if __name__ == "__main__":

    app.run_server(host="0.0.0.0", port=8050, debug=False)
