from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import SessionLocal
import models 
from schemas import *
from sqlalchemy.orm import Session

from services import actualizar_pedido, actualizar_subtotal, actualizar_total_pedido 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = APIRouter()
templates = Jinja2Templates(directory="templates")
# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/detalles_pedidos", status_code=201)
def create_detalle_pedido(detalle_pedido: DetallePedidoCreate, db: Session = Depends(get_db)):
    db_detalle_pedido = models.DetallePedidoDB(**detalle_pedido.dict())
    db.add(db_detalle_pedido)
    db.commit()
    db.refresh(db_detalle_pedido)
    actualizar_subtotal(db_detalle_pedido.id, db)
    actualizar_total_pedido(db_detalle_pedido.pedido_id, db)
    return {"message": "Detalle de pedido creado"}

@app.post("/detalles_pedidos", status_code=201)
def create_detalle_pedido(detalle_pedido: DetallePedidoCreate, db: Session = Depends(get_db)):
    db_detalle_pedido = models.DetallePedidoDB(**detalle_pedido.dict())
    db.add(db_detalle_pedido)
    db.commit()
    db.refresh(db_detalle_pedido)
    actualizar_pedido(db_detalle_pedido.id, db)
    return {"message": "Detalle de pedido creado"}

@app.put("/detalles_pedidos/{id}")
def update_detalle_pedido(id: int, detalle_pedido: DetallePedidoCreate, db: Session = Depends(get_db)):
    db_detalle_pedido = db.query(models.DetallePedidoDB).filter(models.DetallePedidoDB.id == id).first()
    db_detalle_pedido.pedido_id = detalle_pedido.pedido_id
    db_detalle_pedido.producto_id = detalle_pedido.producto_id
    db_detalle_pedido.cantidad = detalle_pedido.cantidad
    db_detalle_pedido.precio_unitario = detalle_pedido.precio_unitario
    db.commit()
    db.refresh(db_detalle_pedido)
    actualizar_pedido(db_detalle_pedido.id, db)
    return {"message": "Detalle de pedido actualizado"}