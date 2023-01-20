# Importamos las librerias necesarias para trabajar los datasets

import pandas as pd
import numpy as np



# Leemos archivos csv con Python usando el metodo read_csv

amazon = pd.read_csv("https://raw.githubusercontent.com/HX-FNegrete/PI01-Data-Engineering/main/Datasets/amazon_prime_titles-score.csv")

disney = pd.read_csv("https://raw.githubusercontent.com/HX-FNegrete/PI01-Data-Engineering/main/Datasets/disney_plus_titles-score.csv")

hulu = pd.read_csv("https://raw.githubusercontent.com/HX-FNegrete/PI01-Data-Engineering/main/Datasets/hulu_titles-score%20(2).csv")

netflix = pd.read_csv("https://raw.githubusercontent.com/HX-FNegrete/PI01-Data-Engineering/main/Datasets/netflix_titles-score.csv")


# Convierto los archivos csv en dataframes

amazon = pd.DataFrame(amazon)

disney = pd.DataFrame(disney)

hulu = pd.DataFrame(hulu)

netflix = pd.DataFrame(netflix)


# Genero campo id. Cada campo id se compone de la primera letra del nombre de la plataforma.

amazon.insert(0, "id", "a")

disney.insert(0,"id","d")

hulu.insert(0, "id","h")

netflix.insert(0,"id","n")


# Los valores nulos del campo rating son reemplazados por el string “G”

amazon["rating"].fillna("G",inplace=True)

disney["rating"].fillna("G",inplace=True)

hulu["rating"].fillna("G",inplace=True)

netflix["rating"].fillna("G",inplace=True)


# Cambio el formato de la fecha de la columna "date_added" a AAAA-mm-dd

amazon["date_added"] = pd.to_datetime(amazon["date_added"], format='%B %d, %Y')

disney["date_added"] = pd.to_datetime(disney["date_added"], format='%B %d, %Y')

hulu["date_added"] = pd.to_datetime(hulu["date_added"], format='%B %d, %Y')

netflix['date_added'] = pd.to_datetime(netflix['date_added'], errors = 'coerce')



# Cambio los campos de texto, de mayusculas a minusculas.
# DF de amazon

amazon["type"] = amazon["type"].str.lower()
amazon["title"] = amazon["title"].str.lower()
amazon["director"] = amazon["director"].str.lower()
amazon["cast"] = amazon["cast"].str.lower()
amazon["country"] = amazon["country"].str.lower()
amazon["listed_in"] = amazon["listed_in"].str.lower()
amazon["description"] = amazon["description"].str.lower()

# DF de disney

disney["type"] = disney["type"].str.lower()
disney["title"] = disney["title"].str.lower()
disney["director"] = disney["director"].str.lower()
disney["cast"] = disney["cast"].str.lower()
disney["country"] = disney["country"].str.lower()
disney["listed_in"] = disney["listed_in"].str.lower()
disney["description"] = disney["description"].str.lower()


# DF de hulu

hulu["type"] = hulu["type"].str.lower()
hulu["title"] = hulu["title"].str.lower()
hulu["director"] = hulu["director"].str.lower()
hulu["country"] = hulu["country"].str.lower()
hulu["listed_in"] = hulu["listed_in"].str.lower()
hulu["description"] = hulu["description"].str.lower()

# DF de netflix


netflix["type"] = netflix["type"].str.lower()
netflix["title"] = netflix["title"].str.lower()
netflix["director"] = netflix["director"].str.lower()
netflix["cast"] = netflix["cast"].str.lower()
netflix["country"] = netflix["country"].str.lower()
netflix["listed_in"] = netflix["listed_in"].str.lower()
netflix["description"] = netflix["description"].str.lower()



# Convierto el campo duration en dos: "duration_int" y "duration_type". El primero será un integer y el segundo un  string indicando la unidad
#  de medición de duración: min (minutos) o season (temporadas)

amazon[['duration_int', 'duration_type']] = amazon['duration'].str.split(' ', n=-1, expand=True, regex=None)
amazon = amazon[amazon.columns[:10].tolist() + ['duration_int', 'duration_type'] + amazon.columns[10:-2].tolist()]

disney[['duration_int', 'duration_type']] = disney['duration'].str.split(' ', n=-1, expand=True, regex=None)
disney = disney[disney.columns[:10].tolist() + ['duration_int', 'duration_type'] + disney.columns[10:-2].tolist()]


hulu[['duration_int', 'duration_type']] = hulu['duration'].str.split(' ', n=-1, expand=True, regex=None)
hulu = hulu[hulu.columns[:10].tolist() + ['duration_int', 'duration_type'] + hulu.columns[10:-2].tolist()]


netflix[['duration_int', 'duration_type']] = netflix['duration'].str.split(' ', n=-1, expand=True, regex=None)
netflix = netflix[netflix.columns[:10].tolist() + ['duration_int', 'duration_type'] + netflix.columns[10:-2].tolist()]



# Hago un "Union" con los datasets ya transformados

df = pd.concat([amazon,disney,hulu,netflix])


# Consulta Nª1
# 1-Cantidad de veces que aparece una keyword en el título de peliculas/series, por plataforma

def keyword_en_titulo(nombre):
    if nombre == "": 
      return {"message":"No se ha especificado el keyword a buscar"}, 404
    else:
      respuesta = {"keyword":nombre,
                   "plataformas":[] 
                  }
      for plat in ['a','n','h','d']:
        datos_locales = df[df['id'].str.startswith(plat, na=False)]
        datos_locales = datos_locales[datos_locales['title'].str.contains(nombre, na=False, regex=False)]

        match plat:
          case 'a':
            nombre = 'Amazon'
          case 'n':
            nombre = 'Netflix'
          case 'h':
            nombre = 'Hulu'
          case _:
            nombre = 'Disney'

        cant = datos_locales.shape[0]
        if cant > 0:
          respuesta['plataformas'].append({"nombre":nombre,"cantidad":cant})
        
      return respuesta   



# Consulta Nª2
# 2- Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año

def score_score_year_plataforma(puntaje,año,plataforma):
    if (plataforma != '') and (int(puntaje) == puntaje) and (int(año) == año)\
       and ((plataforma.lower() == 'disney') or (plataforma.lower() == 'hulu')\
       or (plataforma.lower() == 'amazon') or (plataforma.lower() == 'netflix')):
      respuesta = {"plataforma":plataforma,
                   "score >": puntaje,
                   "year": año
                  }
      datos_locales = df[df['id'].str.startswith(plataforma[0].lower(), na=False)]
      datos_locales = datos_locales[datos_locales['release_year'] == año]
      datos_locales = datos_locales[datos_locales['score'] > puntaje]
      respuesta['cantidad'] = datos_locales.shape[0]
      
      return respuesta
    else:
      return {"message":"Error, parametros incorrectos"} 


# Consulta Nª3
# 3- La segunda película con mayor score para una plataforma determinada, según el orden alfabético de los títulos.

def second_score_plataforma(plataforma):
  if (plataforma != '') and ((plataforma.lower() == 'disney') or (plataforma.lower() == 'hulu')\
    or (plataforma.lower() == 'amazon') or (plataforma.lower() == 'netflix')):
      local_data = df[df['id'].str.startswith('a', na=False)]
      local_data = local_data[local_data['score'] == local_data['score'].max()]
      if len(local_data) > 0:
        local_data = local_data.sort_values(by='title', ascending=True, na_position='first')
      
        score = local_data.iloc[1]['score']
        title = local_data.iloc[1]['title']

        respuesta = {"plataforma":plataforma,
                     "title": str(title),
                     "score": str(score)
                    }
        return respuesta
      return {"message":"No existen datos para esa plataforma"}
  return {"message":"Error, parametros incorrectos"}    



# Consulta Nª4
# 4- Película que más duró según año, plataforma y tipo de duración

def mayor_duracion_con_type(duration_type):
  if (str(duration_type).lower() == 'season') or (str(duration_type).lower() == 'min'):
    respuesta = {"duration_type":duration_type
                }
    for plat in ['n','h','d','a']:
      local_data = df[df['id'].str.startswith(plat, na=False)]
      local_data = local_data[local_data['duration_type'] == duration_type]
      local_data = local_data.sort_values(by='release_year', ascending=True, na_position='first')
      lista_year = list(local_data['release_year'].unique())

      match plat:
        case 'a':
          nombre = 'Amazon'
        case 'n':
          nombre = 'Netflix'
        case 'h':
          nombre = 'Hulu'
        case _:
          nombre = 'Disney'
      respuesta[nombre] = []

      for anno in lista_year:
        local_data1 = local_data[local_data['release_year'] == anno]
        local_data1 = local_data1.sort_values(by='duration_int', ascending=False, na_position='last')
        respuesta[nombre].append({
                                         "año": str(anno),
                                         "nombre": local_data1.iloc[0]['title'],
                                         "duracion": str(local_data1.iloc[0]['duration_int'])
                                       })
    return respuesta                                   
  else:
    return {"message":"Error, parametros incorrectos"}  



# Consulta Nª5
# 5- Cantidad de series y películas por rating

def cant_movie_serie(lista):
    '''Cantidad de series y películas por rating'''
    lista = df['rating'].unique()
    respuesta = {}
    for rate in lista:
        respuesta = {**respuesta, rate:{"movie":str(df[(df['rating'] == rate) & (df['type'] == 'movie')]['id'].count()),
                                        "tv show":str(df[(df['rating'] == rate) & (df['type'] == 'tv show')]['id'].count())
                                       }}
    return respuesta