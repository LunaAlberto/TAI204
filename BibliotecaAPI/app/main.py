from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from typing import Literal

app = FastAPI(
    title="API de Biblioteca Digital",
    description="Alberto Luna Rufino",
    version="1.0"
)

class Libro(BaseModel):
    id: int = Field(..., gt=0, description="identificador del libro")
    titulo: str = Field(..., min_length=2, max_length=100,example="el principito")
    anio: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1, desciption="numero de paginas")
    estado: Literal["disponible", "prestado"] = "disponible"
    
    
class Usuario(BaseModel):
    nombre: str = Field(..., min_length=3,example="jonh doe")
    correo: str
    

libros = [
     {"id":1,"titulo":"Cuando no queden más estrellas que contar","year":2021,"paginas":250,"estado":"disponible"},
     {"id":2,"titulo":"El color de las cosas invisibles","year":2023,"paginas":350,"estado":"disponible"}
]

@app.get("/", tags=["Inicio"])
async def inicio():
    return{"mensaje":"bienvenido a mi biblioteca :)"}
    
@app.get("/v1/libros/", tags=["Biblioteca"])
async def listar_libros():
    return {"status": "200", "total": len(libros), "libros": libros}


@app.post("/v1/libros/", status_code=status.HTTP_201_CREATED, tags=["Biblioteca"])
async def registrar_libro(libro: Libro):
    for l in libros:
        if l["id"] == libro.id:
            raise HTTPException(status_code=400, detail="el id ya existe elije otro difrente")
        
    libros.append(libro.dict())
    return{"mensaje":"el libro ya fue registrado corectamente", "libro": libro}



@app.get("/v1/libros/buscar/", tags=["Biblioteca"])
async def buscar_libro(titulo: str):
    for lib in libros:
        if lib["titulo"].lower() == titulo.lower():
            return {"status": "200","mensaje":"libro encontrado", "libro": lib}
    raise HTTPException(status_code=404, detail="libro no encontrado")



@app.post("/v1/prestamos/{id_libro}", tags=["Acciones"])
async def prestar_libro(id_libro: int, usuario: Usuario):
    for lib in libros:
        if lib["id"] == id_libro:
            if lib["estado"] == "prestado":
                raise HTTPException(status_code=409, detail="el libro ya esta prestado")
            lib["estado"] = "prestado"
            return {"mensaje": f"Libro prestado a {usuario.nombre}", "libro": lib["titulo"]}
    raise HTTPException(status_code=404, detail="El libro no existe")


    
@app.put("/v1/devolucion/{id_libro}", tags=["Acciones"])
async def devolver_libro(id_libro: int):
        for lib in libros:
            if lib["id"] == id_libro:
                if lib["estado"] == "disponible":
                    raise HTTPException(status_code=409, detail="el registro de prestamo no existe")
                lib["estado"] = "disponible"
                return {"status": "200", "mensaje": "libro devuelto exitosamente"}
            
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    

@app.delete("/v1/prestamos/{id_libro}", tags=["Acciones"])
async def eliminar_prestamo(id_libro: int):
    for lib in libros:
        if lib["id"] == id_libro:
            if lib["estado"] == "disponible":
                raise HTTPException(status_code=404, detail="No hay un prestamo activo para este libro")
            lib["estado"] = "disponible"
            return {"mensaje": "registro de prestamo eliminado y libro marcado como disponible"}
    raise HTTPException(status_code=404, detail="Libro no encontrado")







