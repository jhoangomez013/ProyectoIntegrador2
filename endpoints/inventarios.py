from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from auth import get_current_user
from database import SessionLocal
import models 
from schemas import *
from sqlalchemy.orm import Session
from services import tiene_permiso 
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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

# Endpoint Inventarios
@app.get("/inventarios", response_model=List[Inventario])
def get_inventarios(db: Session = Depends(get_db)):
    return db.query(models.InventarioDB).all()

@app.get("/inventarios")
def get_inventarios(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token, db)
    permiso = db.query(models.PermisoDB).filter(models.PermisoDB.nombre == "Inventarios").first()
    if permiso and tiene_permiso(current_user.id, permiso.id, db):
        return db.query(models.InventarioDB).all()
    raise HTTPException(status_code=403, detail="No tienes permiso para ver inventarios")

@app.post("/inventarios", status_code=201)
def create_inventario(inventario: InventarioCreate, db: Session = Depends(get_db)):
    try:
        # Verificar si el producto existe
        db_producto = db.query(models.ProductoDB).filter(models.ProductoDB.id == inventario.producto_id).first()
        if db_producto is None:
            raise HTTPException(status_code=400, detail="Producto no encontrado")

        db_inventario = models.InventarioDB(**inventario.dict())
        db.add(db_inventario)
        db.commit()
        db.refresh(db_inventario)
        return {"message": "Inventario creado"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al crear inventario")

@app.get("/inventarios/{id}", response_model=Inventario)
def get_inventario(id: int, db: Session = Depends(get_db)):
    return db.query(models.InventarioDB).filter(models.InventarioDB.id == id).first()

@app.put("/inventarios/{id}")
def update_inventario(id: int, inventario: Inventario, db: Session = Depends(get_db)):
    db_inventario = db.query(models.InventarioDB).filter(models.InventarioDB.id == id).first()
    db_inventario.producto_id = inventario.producto_id
    db_inventario.cantidad = inventario.cantidad
    db.commit()
    db.refresh(db_inventario)
    return {"message": "Inventario actualizado"}

@app.delete("/inventarios/{id}")
def delete_inventario(id: int, db: Session = Depends(get_db)):
    db_inventario = db.query(models.InventarioDB).filter(models.InventarioDB.id == id).first()
    db.delete(db_inventario)
    db.commit()
    return {"message": "Inventario eliminado"}