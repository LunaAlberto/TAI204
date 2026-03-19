
from fastapi import FastAPI, status, HTTPException,Depends,APIRouter
#importar la base de datos 
from app.data.database import usuarios
#importar el modelo de datos en este caso la clase de crear usuario
from app.models.usuarios import crear_usuario

#seguridad importamos 
from app.security.auth import verificar_peticion
from typing import Optional


#ahora vamos a arreglar la parte del error de app para ello vamos a hacer lo siguiente 
# no creamos una instancia del servidor lo que aremos es poner una aapi router paaraa que este pongaa un
# listado de tododos los anpoints dospinibles 

router = APIRouter(
    prefix="/v1/usuarios", 
    tags=["CRUD HTTP"]
)

#le decimos al servidor que tenemos unos enpitns disponibles
#dentro del api router vamos a definir el primer palamrtro como prefigo 
#el app se repite en toas ls rutas y se repite lo de /v1/usuarioeste sera nuestro prefijo



@router.get("/")
async def consultaT():
    return{
      
        "status":"200",
        "total":len(usuarios),
        "usuarios":usuarios
          
    }
    


@router.post("/")  
async def agregar_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400, 
                  detail="el id ya existe"
            )
    usuarios.append(usuario.dict())
    return{
        "mensaje":"usuario agregado",
        "Usuario" :usuario,
        "status":"200"
    }
    
  
@router.put("/") 
async def actualizar_usuarios(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            usr.update(usuario)
            return{
                "mensaje":"usuario actualizado",
                "usuario":usr,
                "status":"200"
            }
    raise HTTPException(
        status_code=404,
        detail="usuario no encontrado"
    )
    
 
    
    
@router.delete("/{id}")
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_peticion)):

    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": f"usuario eliminado por {usuarioAuth}",
                "status": 200
            }

    raise HTTPException(
        status_code=404,
        detail="usuario no encontrado"
    )
    