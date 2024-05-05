from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()

class Articulo(BaseModel):
    id: int
    titulo: str
    autor: str
    contenido: str
    creado: datetime = datetime.now()
    categoria: str

articulos = []

templates = Jinja2Templates(directory="templates")

@app.post("/crear_articulo/")
async def crear_articulo(articulo: Articulo):
    # Verificar si el ID proporcionado ya está en uso
    for art in articulos:
        if art.id == articulo.id:
            raise HTTPException(status_code=400, detail=f"El ID {articulo.id} ya está en uso.")
    
    # Agregar el artículo a la lista de artículos
    articulos.append(articulo)
    
    return {"mensaje": "Artículo creado exitosamente", "id": articulo.id}

@app.get("/leer_articulo/{id}")
async def leer_articulo(id: int):
    for art in articulos:
        if art.id == id:
            return art
    raise HTTPException(status_code=404, detail="Artículo no encontrado")

@app.put("/modificar_articulo/{id}")
async def modificar_articulo(id: int, articulo: Articulo):
    for i, art in enumerate(articulos):
        if art.id == id:
            articulos[i] = articulo
            return {"mensaje": "Artículo modificado exitosamente"}
    raise HTTPException(status_code=404, detail="Artículo no encontrado")

@app.delete("/borrar_articulo/{id}")
async def borrar_articulo(id: int):
    for i, art in enumerate(articulos):
        if art.id == id:
            del articulos[i]
            return {"mensaje": "Artículo borrado exitosamente"}
    raise HTTPException(status_code=404, detail="Artículo no encontrado")

@app.get("/", response_class=HTMLResponse)
async def mostrar_articulos(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "articulos": articulos})
