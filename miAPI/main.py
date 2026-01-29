#importaciones
from fastapi import FastAPI
import asyncio

#instancia del servidor
#preparar todo el servidor con laas ventajas que ofrece fastapi 
app=FastAPI()



#Endpoints 
@app.get("/")
#endpoint de inicio es la ruta con la que arrncara el servidor
async def bienvenido():
    return{"mesage":"Bienvenido a fastapi"}
#lado izquirdo clave 
#lado derecho el vamor en este caso clase es mensaje= valor igual a bienvenido a fastapi

#hasta aqui ya tenemos nuestro servidor ya esta funcionado 

#correr un servidor tenemos que ir a nuestra terminal

#segundo endpoint 

@app.get("/holamundo")
async def hola():
    await asyncio.sleep(5)
    return{"mesage":"Bienvenido a fastapi",
           "status":"200"
           }