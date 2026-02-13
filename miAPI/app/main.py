#importaciones
from fastapi import FastAPI
import asyncio
#importamos 
from typing import Optional

#instancia del servidor
#preparar todo el servidor con laas ventajas que ofrece fastapi 
app=FastAPI(
    title="Mi primer API",
    description="Alberto Luna Rufino",
    version="1.0"   
)

#tabla ficticia solo para verificar 
#datos para ver como nos responderia un diccionario de usuarios

usuarios=[
    {"id":1,"nombre":"Alberto","edad":20},
    {"id":2,"nombre":"Diego","edad":20},
    {"id":3,"nombre":"Jochua","edad":20}
]



#Endpoints 
@app.get("/",tags=["inicio"])
#endpoint de inicio es la ruta con la que arrncara el servidor
async def bienvenido():
    return{"mesage":"Bienvenido a fastapi"}
#lado izquirdo clave 
#lado derecho el vamor en este caso clase es mensaje= valor igual a bienvenido a fastapi

#hasta aqui ya tenemos nuestro servidor ya esta funcionado 

#correr un servidor tenemos que ir a nuestra terminal

#segundo endpoint 

@app.get("/holamundo",tags=["Asincronia"])
async def hola():
    await asyncio.sleep(5)
    return{"mesage":"Bienvenido a fastapi",
           "status":"200"
           }
    
    
    
#Endpoints creamos otro Endpoints lo que tenemos en cuenta es que los parametros lo estamos 
#solicitando entre llaves  en este caso le decimos que para que v1 funcione es obligatorio un id 
#nos aseguramos que el id se obligatorio y que lleve con el formato que necvesitamos en este caso 
#sera entero es el mas comun 
#el id que llegue sera entero y para poder pasar la va;idacion tiene que ser entero
#cuidar las , por que son objetos JSON
@app.get("/v1/usuario/{id}",tags=["parametro obligatorio"])
#endpoint de inicio es la ruta con la que arrncara el servidor
async def consultauno(id:int):
    return{"mesage":"usuario encontrado","usuario":id,"status":"200"}

#obligatorio que el paramtro este en el endpoint
    
    
    
    #4
    #no puede aver dos enpoints con el mismo nombre en este caso si los dos son get 
    #no pueden aver dos con el mismo nombre al menos que sean delete
    #aguas con las llaves por que no es oblitario este caso no es obligatorio 
    #y la funcion tiene que ser otro nombre por que si no reutilizamos la funcion del otro 
    #optional[int]= None puede que venga o no venga un dato y en caso de que no 
    #lo declaramos como nulo
    
@app.get("/v1/usuarios/",tags=["parametro obligatorio"])
#endpoint de inicio es la ruta con la que arrncara el servidor
async def consultatodos(id:Optional[int]=None):
    if id is not None:
        #verificamos si el id no es nulo con is not None  
        # si no es nulo quiere decir que viene con un valor 
        #recorremos con un for es la llave que va recorrriendo el for 
        #recorremos con usuarioK en la tabla usuarios
        
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
             return{"mesage":"usuario encontrado", "usuario":usuarioK,"status":"200"}
            
            #caso donde si encontre al usuario en este caso si lo encontre
            #si el for acaba y nose encontro el usuario enconces se ejecuta el return de abajo
        
            
        return {"mesage":"usuario no encontrado"}
    
    #esto es por si el usuario no ingreso ningun id en el endpoint
    #si el id es nulo osea que no se proporciono ningun id en el endpoint se ejecuta este return
    else:
        return{"message":"no se proporciono el id"}
    
    