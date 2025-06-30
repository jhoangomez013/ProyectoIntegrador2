
from fastapi import APIRouter, Request, Depends
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

#Endpoint Porductos
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.get("/productos", response_model=List[Producto])
def get_productos(db: Session = Depends(get_db)):
    return db.query(models.ProductoDB).all()

@app.post("/productos", status_code=201)
def create_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = models.ProductoDB(**producto.dict(exclude_unset=True))
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return {"message": "Producto creado"}
@app.get("/productos/{id}", response_model=Producto)
def get_producto(id: int, db: Session = Depends(get_db)):
    return db.query(models.ProductoDB).filter(models.ProductoDB.id == id).first()

@app.put("/productos/{id}")
def update_producto(id: int, producto: Producto, db: Session = Depends(get_db)):
    db_producto = db.query(models.ProductoDB).filter(models.ProductoDB.id == id).first()
    db_producto.nombre = producto.nombre
    db_producto.descripcion = producto.descripcion
    db_producto.precio = producto.precio
    db.commit()
    db.refresh(db_producto)
    return {"message": "Producto actualizado"}

@app.delete("/productos/{id}")
def delete_producto(id: int, db: Session = Depends(get_db)):
    db_producto = db.query(models.ProductoDB).filter(models.ProductoDB.id == id).first()
    db.delete(db_producto)
    db.commit()

    return {"message": "Producto eliminado"}