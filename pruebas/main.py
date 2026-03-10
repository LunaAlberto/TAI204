from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel,Field


app=FastAPI(
    title="Mi primer API",
    description="Alberto Luna Rufino",
    version="1.0")

@app.get("/",tags=["inicio"])
def inicio():
    return "Bienvenido a mi primera API con Flask"


if __name__ == '__main__':
    app.run(debug=True, port=5005)
#uvicorn main:app --reload
#python3 app.py
#docker-compose up --build

