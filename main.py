from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session 
from database import SessionLocal, engine
import models 
from models import AnotacionDB, DetallePedidoDB, PedidoDB
from services import actualizar_pedido, actualizar_subtotal, actualizar_total_pedido, calcular_total_pedido
from schemas import *
from endpoints import productos, pedidos, anotaciones, rol_permiso, usuarios, inventarios, detalle_pedido, permisos, rol, login

# Crea las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)
# Dependencia para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear la aplicación FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates")
# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

#Endpoint Porductos
app.include_router(productos.app)

# Endpoint Pedidos
app.include_router(pedidos.app)

# Endpoint Anotaciones
app.include_router(anotaciones.app)

# Endpoint Usuarios
app.include_router(usuarios.app)

# Endpoint Inventarios
app.include_router(inventarios.app)

# Endpoint Detalle de pedidos
app.include_router(detalle_pedido.app)

# Endpoin Permisos
app.include_router(permisos.app)

# Endpoin Roles_Permiso
app.include_router(rol_permiso.app)

# Endpoin Roles
app.include_router(rol.app)

# Endpoin Login
app.include_router(login.app)



