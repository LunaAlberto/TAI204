from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import datetime, time
import secrets
from enum import Enum

app = FastAPI(
    title="API de bancos",
    description="Alberto Luna Rufino",
    version="1.0"
)

security = HTTPBasic()

turnos_db = []
siguiente_id = 1

def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(security)):
    usuarioAuth = secrets.compare_digest(credenciales.username, "banco")
    contraAuth = secrets.compare_digest(credenciales.password, "2468")
    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="credenciales no autorizadas"
        )
    return credenciales.username

class TipoTramite(str, Enum):
    deposito = "deposito"
    retiro = "retiro"
    consulta = "consulta"

class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=8, max_length=100)

class TurnoCreate(BaseModel):
    id: int = Field(..., gt=0, description="identificador")
    cliente: str = Field(..., min_length=8)
    tipo_tramite: TipoTramite
    fecha: str
    hora: str
    @validator('hora')
    def validar_hora(cls, v):
        try:
            h, m = map(int, v.split(':'))
            if h < 9 or h > 15:
                raise ValueError('Hora debe estar entre 09:00 y 15:00')
            if h == 15 and m > 0:
                raise ValueError('Hora debe estar entre 09:00 y 15:00')
        except:
            raise ValueError('Formato de hora invalido (HH:MM)')
        return v

class Turno(TurnoCreate):
    id: int
    estado: str = "pendiente"
    fecha_creacion: str

class TurnoUpdate(BaseModel):
    estado: str

@app.get("/", tags=["inicio"])
def inicio():
    return {"mensaje": "Bienvenido a la API de Turnos Bancarios"}

@app.post("/turnos", response_model=Turno, tags=["turnos"], status_code=status.HTTP_201_CREATED)
def crear_turno(turno: TurnoCreate, usuario: str = Depends(verificar_peticion)):
    global siguiente_id
    turnos_hoy = [t for t in turnos_db if t.get('cliente') == turno.cliente and t.get('fecha') == turno.fecha]
    if len(turnos_hoy) >= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se permiten mas de 5 turnos por día para este cliente"
        )
    nuevo_turno = {
        "id": siguiente_id,
        "cliente": turno.cliente,
        "tipo_tramite": turno.tipo_tramite,
        "fecha": turno.fecha,
        "hora": turno.hora,
        "estado": "pendiente",
        "fecha_creacion": datetime.now().isoformat()
    }
    turnos_db.append(nuevo_turno)
    siguiente_id += 1
    return nuevo_turno

@app.get("/turnos", response_model=List[Turno], tags=["turnos"])
def listar_turnos(usuario: str = Depends(verificar_peticion)):
    return turnos_db

@app.get("/turnos/{turno_id}", response_model=Turno, tags=["turnos"])
def obtener_turno(turno_id: int, usuario: str = Depends(verificar_peticion)):
    turno = next((t for t in turnos_db if t.get('id') == turno_id), None)
    if not turno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turno no encontrado"
        )
    return turno

@app.put("/turnos/{turno_id}/atendido", response_model=Turno, tags=["turnos"])
def marcar_atendido(turno_id: int, usuario: str = Depends(verificar_peticion)):
    turno = next((t for t in turnos_db if t.get('id') == turno_id), None)
    if not turno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turno no encontrado"
        )
    turno['estado'] = "atendido"
    return turno

@app.delete("/turnos/{turno_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["turnos"])
def eliminar_turno(turno_id: int, usuario: str = Depends(verificar_peticion)):
    global turnos_db
    turno = next((t for t in turnos_db if t.get('id') == turno_id), None)
    if not turno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turno no encontrado"
        )
    turnos_db = [t for t in turnos_db if t.get('id') != turno_id]
    return None