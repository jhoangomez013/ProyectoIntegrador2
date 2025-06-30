
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from Base_De_Datos.database import SessionLocal
from Base_De_Datos import models 
from schemas import *
from sqlalchemy.orm import Session

from services import calcular_total_pedido 

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

# Endpoint Pedidos
@app.get("/pedidos", response_model=List[Pedido])
def get_pedidos(db: Session = Depends(get_db)):
    return db.query(models.PedidoDB).all()

@app.get("/pedidos/{id}", response_model=PedidoConAnotaciones)
def get_pedido(id: int, db: Session = Depends(get_db)):
    pedido = db.query(models.PedidoDB).filter(models.PedidoDB.id == id).first()
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    anotaciones = db.query(models.AnotacionDB).filter(models.AnotacionDB.pedido_id == id).all()
    pedido.anotaciones = anotaciones
    return pedido

@app.get("/pedidos/{pedido_id}/total")
async def get_total_pedido(pedido_id: int, db: Session = Depends(get_db)):
    total = calcular_total_pedido(pedido_id, db)
    return {"total": total}

@app.post("/pedidos", status_code=201)
def create_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    db_pedido = models.PedidoDB(**pedido.dict())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return {"message": "Pedido creado"}

@app.post("/pedidos/{pedido_id}/productos", status_code=201)
def agregar_producto_pedido(pedido_id: int, producto_id: int, cantidad: int, db: Session = Depends(get_db)):
    producto = db.query(models.ProductoDB).filter(models.ProductoDB.id == producto_id).first()
    precio_unitario = producto.precio
    subtotal = precio_unitario * cantidad

    detalle_pedido = models.DetallePedidoDB(
        pedido_id=pedido_id,
        producto_id=producto_id,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        subtotal=subtotal
    )
    db.add(detalle_pedido)
    db.commit()
    db.refresh(detalle_pedido)
    return {"message": "Producto agregado al pedido"}

@app.put("/pedidos/{id}")
def update_pedido(id: int, pedido: Pedido, db: Session = Depends(get_db)):
    db_pedido = db.query(models.PedidoDB).filter(models.PedidoDB.id == id).first()
    db_pedido.fecha = pedido.fecha
    db_pedido.total = pedido.total
    db.commit()
    db.refresh(db_pedido)
    return {"message": "Pedido actualizado"}

@app.delete("/pedidos/{id}")
def delete_pedido(id: int, db: Session = Depends(get_db)):
    db_pedido = db.query(models.PedidoDB).filter(models.PedidoDB.id == id).first()
    db.delete(db_pedido)
    db.commit()
    return {"message": "Pedido eliminado"}