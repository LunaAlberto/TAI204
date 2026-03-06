from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel,Field

#nuevas lineas 

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

#nuevas lineas
SECRET_KEY = "alberto"
ALGORITHM = "HS256"
MINUTES_EXPIRE = 1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



app=FastAPI(
    title="Mi primer API",
    description="Alberto Luna Rufino",
    version="1.0"   
)

# estas lineas nos ayuda a crear el token de autenticacion
def crear_token(data: dict):
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=MINUTES_EXPIRE)
    payload = data.copy()
    payload.update({"exp": expiracion})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def validar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException( 
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="token esxpirado"
            )


usuarios=[
    {"id":1,"nombre":"Alberto","edad":20},
    {"id":2,"nombre":"Diego","edad":20},
    {"id":3,"nombre":"Jochua","edad":20}
]


@app.post("/token", tags=["autenticacion"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "alberto" and form_data.password == "123456":
        token = crear_token({"sub": form_data.username})
        return {
            "access_token": token,
            "token_type": "bearer",
            "mensaje": f"Bienvenido {form_data.username}, tu acceso ha sido concedido."
        }
    raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")




class crear_usuario(BaseModel):
    id:int = Field(..., gt=0, description="identificador de usuario")
    nombre:str= Field(...,min_length=3, max_length=50, example="Joohn Doe")
    edad:int=Field(...,gt=1,le=125,description="edad valida entre 1 y 125")

@app.get("/",tags=["inicio"])

async def bienvenido():
    return{"mesage":"Bienvenido a fastapi"}

@app.get("/holamundo",tags=["Asincronia"])
async def hola():
    await asyncio.sleep(5)
    return{"mesage":"Bienvenido a fastapi",
           "status":"200"
           }
    
@app.get("/v1/usuarioOb/{id}",tags=["parametro obligatorio"])

async def consultauno(id:int):
    return{"mesage":"usuario encontrado","usuario":id,"status":"200"}
   
@app.get("/v1/usuariosOp/",tags=["parametro obligatorio"])

async def consultatodos(id:Optional[int]=None):
    if id is not None:

        
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
             return{"mesage":"usuario encontrado", "usuario":usuarioK,"status":"200"}
      
        return {"mesage":"usuario no encontrado"}
   
    else:
        return{"message":"no se proporciono el id"}
    
    
@app.get("/v1/usuarios/",tags=['CRUD HTTP'])
async def consultaT():
    return{

        "status":"200",
        "total":len(usuarios),
        "usuarios":usuarios
          
    }
    
   
@app.post("/v1/usuarios/",tags=['CRUD HTTP'])  
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

@app.put("/v1/usuarios/",tags=['CRUD HTTP']) 
async def actualizar_usuarios(usuario:crear_usuario, usuario_autenticado: str = Depends(validar_token)):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            usr.update(usuario.dict())
            return{
                "mensaje":f"usuario actualizado por {usuario_autenticado} ",
                "usuario":usr,
                "status":"200"
            }
    raise HTTPException(
        status_code=404,
        detail="usuario no encontrado"
    )

    
@app.delete("/v1/usuarios/", tags=['CRUD HTTP'])
async def eliminar_usuario(id: int, usuario_autenticado: str = Depends(validar_token)):

    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": f"usuario eliminado por:{usuario_autenticado}",
                "status": 200
            }

    raise HTTPException(
        status_code=404,
        detail="usuario no encontrado"
    )
    
    
    
    
    
    
    
    
    
    
    
   