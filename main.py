from fastapi import FastAPI
import pandas as pd 
from ETLPI1 import df



PI1 = FastAPI(title="Proyecto individual Nª1 de Henry")

# Consulta Nª1
# 1-Cantidad de veces que aparece una keyword en el título de peliculas/series, por plataforma

@PI1.get("/keyword_en_titulo/")
async def keyword_en_titulo(nombre):

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

@PI1.get("/Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año/")
async def score_score_year_plataforma(puntaje:int,año:int,plataforma:str):

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

@PI1.get("/La segunda película con mayor score para una plataforma determinada, según el orden alfabético de los títulos/")
async def second_score_plataforma(plataforma):
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

@PI1.get("/Película que más duró según año, plataforma y tipo de duración/")
async def get_longest(plataforma:str,duration_tipo:str,date:int):
    plataformas = {"netflix":"n","amazon":"a","hulu":"h","disney":"d"}
    df_temp = df[(df['id'].str[0] == plataformas[plataforma])&(df['release_year']==date)&(df['duration_type']==duration_tipo)&\
          (df['type']=='movie')].sort_values(['duration_int'], ascending=False).reset_index(drop=True)[["title","duration_int","duration_type"]].iloc[0,:]
    return df_temp.to_dict()


# Consulta Nª5
# 5- Cantidad de series y películas por rating

@PI1.get("/Cantidad de series y películas por rating/")
async def cant_movie_serie(lista):
    '''Cantidad de series y películas por rating'''
    lista = df['rating'].unique()
    respuesta = {}
    for rate in lista:
        respuesta = {**respuesta, rate:{"movie":str(df[(df['rating'] == rate) & (df['type'] == 'movie')]['id'].count()),
                                        "tv show":str(df[(df['rating'] == rate) & (df['type'] == 'tv show')]['id'].count())
                                       }}
    return respuesta