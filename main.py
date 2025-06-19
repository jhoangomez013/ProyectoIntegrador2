from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session 
from database import SessionLocal, engine
import models

# Crea las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)
# Dependencia para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Modelo de datos de los celulares utilizando Pydantic

class Producto(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float

class Pedido(BaseModel):
    id: int
    fecha: str
    total: float

class Anotacion(BaseModel):
    id: int
    pedido_id: int
    texto: str

class Anexo(BaseModel):
    id: int
    pedido_id: int
    archivo: str

class Usuario(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    password: str

class Inventario(BaseModel):
    id: int
    producto_id: int
    cantidad: int

    class Config:
        orm_mode = True
# Crear la aplicación FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates")
# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.get("/productos", response_model=List[Producto])
def get_productos(db: Session = Depends(get_db)):
    return db.query(models.ProductoDB).all()

@app.post("/productos", status_code=201)
def create_producto(producto: Producto, db: Session = Depends(get_db)):
    db_producto = models.ProductoDB(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return {"message": "Producto creado"}
# Eliminar un celular
@app.delete("/celulares/{id}")
def delete_celular(id: str, db: Session = Depends(get_db)):
    celular = db.query(models.CelularDB).filter(models.CelularDB.id == id).first()
    if not celular:
        raise HTTPException(status_code=404, detail="Celular no encontrado")
    db.delete(celular)
    db.commit()
    return {"message": "Celular eliminado"}
# Actualizar un celular
@app.put("/celulares/{id}")
def update_celular(id: str, celular: Celular, db: Session = Depends(get_db)):
    celular_db = db.query(models.CelularDB).filter(models.CelularDB.id == id).first()
    if not celular_db:
        raise HTTPException(status_code=404, detail="Celular no encontrado")
    celular_db.marca = celular.marca
    celular_db.modelo = celular.modelo
    db.commit()
    return {"message": "Celular actualizado"}


#seccion de clientes
@app.get("/clientes", response_model=List[Cliente])
def get_clientes(db: Session = Depends(get_db)):
    return db.query(models.ClienteDB).all()

@app.post("/clientes", status_code=201)
def create_cliente(cliente: Cliente, db: Session = Depends(get_db)):
    db_cliente = models.ClienteDB(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return {"message": "Cliente creado"}

@app.delete("/clientes/{id}")
def delete_cliente(id: str, db: Session = Depends(get_db)):
    cliente = db.query(models.ClienteDB).filter(models.ClienteDB.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(cliente)
    db.commit()
    return {"message": "Cliente eliminado"}

@app.put("/clientes/{id}")
def update_cliente(id: str, cliente: Cliente, db: Session = Depends(get_db)):
    cliente_db = db.query(models.ClienteDB).filter(models.ClienteDB.id == id).first()
    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    cliente_db.nombre = cliente.nombre
    cliente_db.apellido = cliente.apellido
    db.commit()
    return {"message": "Cliente actualizado"}

#Seccion de proveedores
@app.get("/proveedores", response_model=List[Proveedor])
def get_proveedores(db: Session = Depends(get_db)):
    return db.query(models.ProveedorDB).all()

@app.post("/proveedores", status_code=201)
def create_proveedor(proveedor: Proveedor, db: Session = Depends(get_db)):
    db_proveedor = models.ProveedorDB(**proveedor.dict())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return {"message": "Proveedor creado"}

@app.delete("/proveedores/{id}")
def delete_proveedor(id: str, db: Session = Depends(get_db)):
    proveedor = db.query(models.ProveedorDB).filter(models.ProveedorDB.id == id).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    db.delete(proveedor)
    db.commit()
    return {"message": "Proveedor eliminado"}

@app.put("/proveedores/{id}")
def update_proveedor(id: str, proveedor: Proveedor, db: Session = Depends(get_db)):
    proveedor_db = db.query(models.ProveedorDB).filter(models.ProveedorDB.id == id).first()
    if not proveedor_db:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    proveedor_db.nombre = proveedor.nombre
    proveedor_db.direccion = proveedor.direccion
    db.commit()
    return {"message": "Proveedor actualizado"}