
from fastapi import FastAPI, status, HTTPException,Depends,APIRouter
#importar la base de datos 
#from app.data.database import usuarios
#importar el modelo de datos en este caso la clase de crear usuario
from app.models.usuarios import UsuarioCreate, UsuarioUpdate

#seguridad importamos 
from app.security.auth import verificar_peticion
from typing import Optional


#creamos importaciones 

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuarios as usuarioDB


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
async def consultaT(db: Session = Depends(get_db)):
    usuarios = db.query(usuarioDB).all()

    return {
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }


#get  consultar por id 

@router.get("/{id}")
async def consulta_id(id: int, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="usuario no encontrado")

    return {
        "status": "200",
        "usuario": usuario
    }

#post 
@router.post("/")
async def agregar_usuario(usuarioP: UsuarioCreate, db: Session = Depends(get_db)):
    nuevo = usuarioDB(nombre=usuarioP.nombre, edad=usuarioP.edad)

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {
        "mensaje": "usuario agregado",
        "usuario": nuevo
    }
    
#put 

@router.put("/{id}")
async def actualizar_usuario(
    id: int,
    usuarioP: UsuarioCreate,
    usuarioAuth: str = Depends(verificar_peticion),
    db: Session = Depends(get_db)
):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="usuario no encontrado")

    usuario.nombre = usuarioP.nombre
    usuario.edad = usuarioP.edad

    db.commit()
    db.refresh(usuario)

    return {
        "mensaje": f"usuario actualizado por {usuarioAuth}",
        "usuario": usuario
    }


#patch 

@router.patch("/{id}")
async def actualizar_parcial(
    id: int,
    datos: UsuarioUpdate,
    usuarioAuth: str = Depends(verificar_peticion),
    db: Session = Depends(get_db)
):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="usuario no encontrado")

   
    if datos.nombre is not None:
        usuario.nombre = datos.nombre

    if datos.edad is not None:
        usuario.edad = datos.edad

    db.commit()
    db.refresh(usuario)

    return {
        "mensaje": f"usuario actualizado parcialmente por {usuarioAuth}",
        "usuario": usuario
    }


#detele

@router.delete("/{id}")
async def eliminar_usuario(
    id: int,
    usuarioAuth: str = Depends(verificar_peticion),
    db: Session = Depends(get_db)
):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="usuario no encontrado")

    db.delete(usuario)
    db.commit()

    return {
        "mensaje": f"usuario eliminado por {usuarioAuth}"
    }

