#importaciones

from fastapi import FastAPI, APIRouter
#importar los routers el de usuarios y el de varios 
from app.routers import usuarios,varios

app=FastAPI(
    title="Mi primer API",
    description="Alberto Luna Rufino",
    version="1.0"   
)

app.include_router(usuarios.router)
app.include_router(varios.routerV)

