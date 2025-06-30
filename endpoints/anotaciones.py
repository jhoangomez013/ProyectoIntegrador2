
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from Base_De_Datos.database import SessionLocal
from Base_De_Datos import models 
from schemas import *
from sqlalchemy.orm import Session 

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

# Endpoint Anotaciones
@app.get("/pedidos/{pedido_id}/anotaciones", response_model=List[Anotacion])
def get_anotaciones(pedido_id: int, db: Session = Depends(get_db)):
    return db.query(models.AnotacionDB).filter(models.AnotacionDB.pedido_id == pedido_id).all()

@app.post("/pedidos/{pedido_id}/anotaciones", status_code=201)
def create_anotacion(pedido_id: int, anotacion: AnotacionCreate, db: Session = Depends(get_db)):
    if anotacion.pedido_id != pedido_id:
        raise HTTPException(status_code=400, detail="El pedido_id en la anotación no coincide con el pedido_id en la URL")
    db_anotacion = models.AnotacionDB(**anotacion.dict())
    db.add(db_anotacion)
    db.commit()
    db.refresh(db_anotacion)
    return {"message": "Anotación creada"}

@app.get("/pedidos/{pedido_id}/anotaciones/{id}", response_model=Anotacion)
def get_anotacion(pedido_id: int, id: int, db: Session = Depends(get_db)):
    return db.query(models.AnotacionDB).filter(models.AnotacionDB.id == id, models.AnotacionDB.pedido_id == pedido_id).first()

@app.put("/pedidos/{pedido_id}/anotaciones/{id}")
def update_anotacion(pedido_id: int, id: int, anotacion: Anotacion, db: Session = Depends(get_db)):
    db_anotacion = db.query(models.AnotacionDB).filter(models.AnotacionDB.id == id, models.AnotacionDB.pedido_id == pedido_id).first()
    db_anotacion.texto = anotacion.texto
    db.commit()
    db.refresh(db_anotacion)
    return {"message": "Anotación actualizada"}

@app.delete("/pedidos/{pedido_id}/anotaciones/{id}")
def delete_anotacion(pedido_id: int, id: int, db: Session = Depends(get_db)):
    db_anotacion = db.query(models.AnotacionDB).filter(models.AnotacionDB.id == id, models.AnotacionDB.pedido_id == pedido_id).first()
    db.delete(db_anotacion)
    db.commit()
    return {"message": "Anotación eliminada"}