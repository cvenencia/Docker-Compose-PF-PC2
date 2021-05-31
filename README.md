## Proyecto Final Estructura del Computador II

**Enunciado:** https://docs.google.com/document/d/18E5iOsmqbjvs3pNJd8ltrJbR2tu3F7dRsftpKNroIrw/edit?pli=1

**Descripción:**
Se decidió tomar un dataset acorde a la temática actual: covid-19. Para esto, se usó el dataset proveniente del Instituto Nacional de Salud (datos oficiales), haciendo posteriormente una conversión para ingresarlos dentro de la base de datos de Postgres y finalmente, hacer las respectivas visualizaciones por medio de Jupyter Notebooks y Python con Dash.

**Contenedores:**
1. Contenedor con Jupyter-Notebook para mostrar las 3 visualizaciones, así mismo se hace conexión con la base de datos en el contenedor con la imagen de Postgres.
2. Contenedor con Postgres, así como scripts que crean la base de datos de covid-19 en Colombia, dividida en 5 partes por restricciones de tamaño de GitHub (scriptCovid1-5.sql). Estos datos fueron obtenidos de la página oficial del [Instituto Nacional de Salud](https://www.ins.gov.co/Paginas/Inicio.aspx), tomando solamente los primeros 500 mil primeros datos para reducir un poco el tiempo de carga y el tamaño del archivo.
3. Contenedor con Python y librerías para el uso de Dash, generando así las gráficas pertinentes.

En el directorio _datos_ se encuentran tres subdirectorios. Cada uno corresponde a un volumen de tipo bind, los cuales son enviados a cada contenedor. En _NotebooksJupyter_ se encuentra el notebook con las visualizaciones, en _src\_Dash_ se encuentra el archivo .py con las visualizaciones en Dash, y por último, en _scriptSQL_ se encuentran los scripts que ingresan los datos a la base de datos.

**Links Importantes**
[Dataset de Covid en colombia](https://www.datos.gov.co/Salud-y-Protecci-n-Social/Casos-positivos-de-COVID-19-en-Colombia/gt2j-8ykr/data)

