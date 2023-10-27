El proyecto consistió en simular un ambiente de trabajo como data engineer, extrayendo cuatro archivos en formato csv de distintas plataformas para ver películas y series (Amazon, Netflix, Hulu y Disney) a los cuales tuvimos que aplicar el proceso de extracción, transformación y limpieza(E.T.L.) usando Python y su famosa librería "Pandas".
Una vez realizadas las consultas correspondientes a los dataframes finales (como se solicito en la consigna), pasamos a conectar todas las estructuras de código a una Api, mediante FastApi, para disponibilizar toda la información, hacerla publica y que se la pueda consultar de manera sencilla.

# Video
**`Video Demostrativo`** de ***5 minutos*** explicando el trabajo realizado durante este proyecto. <a href=https://drive.google.com/file/d/1prpZ41ZMJeMGFSdmkGXTFen9Q-aLo5KI/view?usp=share_link</a> </strong>

# Deployment
**`Deployment`** con la empresa [Deta](https://www.deta.sh/?ref=fastapi) (no necesita dockerizacion) <a href="https://hwi73g.deta.dev">Deployment</a> </strong>

# Consultas
Estas son las consultas hechas dentro de la aplicacion de FastAPI:
+ Cantidad de veces que aparece una keyword en el título de peliculas/series, por plataforma.

+ Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año.

+ La segunda película con mayor score para una plataforma determinada, según el orden alfabético de los títulos.

+ Película que más duró según año, plataforma y tipo de duración.

+ Cantidad de series y películas por rating.
<br/>
