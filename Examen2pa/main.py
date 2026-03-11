from fastapi import FastAPI, status, HTTPException
from fastapi import FastAPI, status, HTTPException,Depends
import asyncio
from pydantic import BaseModel,Field
from typing import Optional
from  fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import datetime, timedelta, timezone
import secrets

app=FastAPI()

security = HTTPBasic()

def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(security)):

    usuarioAuth = secrets.compare_digest(credenciales.username, "banco")
    contraAuth = secrets.compare_digest(credenciales.password, "2468")

    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="credenciales no autorizadas"
        )

    return credenciales.username

class crear_token(BaseModel):
    id:int = Field(..., gt=0, description="identificador de usuario")
    nombre:str= Field(...,min_length=8, max_length=50, example="Joohn Doe")
    
    

@app.get("/", tags=["inicio"])
def inicio():
    return {"mensaje": "Bienvenido a mi API banco"}




   

