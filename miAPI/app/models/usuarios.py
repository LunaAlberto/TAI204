###crear modelo pydantic de validaciones
#aqui yaa tenemos nuestro modelo pydantic esto es solo paraa crear usuario
#para que pase la parte del pydantic necesita pasar la validacion de 
# los datos que recibimos en el endpoint de crear usuario

#agregamos importaciones 
from pydantic import BaseModel,Field
from typing import Optional

class UsuarioCreate(BaseModel):
    nombre:str= Field(...,min_length=3, max_length=50, example="Joohn Doe")
    edad:int=Field(...,gt=1,le=125,description="edad valida entre 1 y 125")

class UsuarioUpdate(BaseModel):
    nombre:Optional[str]= Field(None,min_length=3, max_length=50, example="Joohn Doe")
    edad:Optional[int]=Field(None,gt=1,le=125,description="edad valida entre 1 y 125")


