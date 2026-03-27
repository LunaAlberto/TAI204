import asyncio
#importamos 
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.data.db import get_db
from app.data.usuario import Usuarios as usuarioDB

routerV = APIRouter(
    prefix="/varios", 
    tags=["Varios"]
)


@routerV.get("/bienvenidos")

async def bienvenido():
    return{"mesage":"Bienvenido a fastapi"}


@routerV.get("/espera")
async def hola():
    await asyncio.sleep(5)
    return{"mesage":"Bienvenido a fastapi",
           "status":"200"
    }
    
@routerV.get("/usuario/{id}")
async def consultauno(id: int, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="usuario no encontrado")

    return {
        "message": "usuario encontrado",
        "usuario": usuario
    }      



           
@routerV.get("/buscar")
async def consultatodos(id: Optional[int] = None, db: Session = Depends(get_db)):

    if id is not None:
        usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

        if not usuario:
            return {"message": "usuario no encontrado"}

        return {
            "message": "usuario encontrado",
            "usuario": usuario
        }

    usuarios = db.query(usuarioDB).all()

    return {
        "message": "lista de usuarios",
        "total": len(usuarios),
        "usuarios": usuarios
    }
    
    