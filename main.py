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




# Endpoint Pedidos
@app.get("/pedidos", response_model=List[Pedido])
def get_pedidos(db: Session = Depends(get_db)):
    return db.query(models.PedidoDB).all()

@app.get("/pedidos/{id}", response_model=PedidoConAnotaciones)
def get_pedido(id: int, db: Session = Depends(get_db)):
    pedido = db.query(PedidoDB).filter(PedidoDB.id == id).first()
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    anotaciones = db.query(AnotacionDB).filter(AnotacionDB.pedido_id == id).all()
    pedido.anotaciones = anotaciones
    return pedido

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





# Endpoint Usuarios
@app.get("/usuarios", response_model=List[Usuario])
def get_usuarios(db: Session = Depends(get_db)):
    return db.query(models.UsuarioDB).all()

@app.post("/usuarios", status_code=201)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = models.UsuarioDB(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return {"message": "Usuario creado"}

@app.get("/usuarios/{id}", response_model=Usuario)
def get_usuario(id: int, db: Session = Depends(get_db)):
    return db.query(models.UsuarioDB).filter(models.UsuarioDB.id == id).first()

@app.put("/usuarios/{id}")
def update_usuario(id: int, usuario: Usuario, db: Session = Depends(get_db)):
    db_usuario = db.query(models.UsuarioDB).filter(models.UsuarioDB.id == id).first()
    db_usuario.nombre = usuario.nombre
    db_usuario.apellido = usuario.apellido
    db_usuario.email = usuario.email
    db_usuario.password = usuario.password
    db.commit()
    db.refresh(db_usuario)
    return {"message": "Usuario actualizado"}

@app.delete("/usuarios/{id}")
def delete_usuario(id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(models.UsuarioDB).filter(models.UsuarioDB.id == id).first()
    db.delete(db_usuario)
    db.commit()
    return {"message": "Usuario eliminado"}


# Endpoint Inventarios
@app.get("/inventarios", response_model=List[Inventario])
def get_inventarios(db: Session = Depends(get_db)):
    return db.query(models.InventarioDB).all()

@app.post("/inventarios", status_code=201)
def create_inventario(inventario: InventarioCreate, db: Session = Depends(get_db)):
    db_inventario = models.InventarioDB(**inventario.dict())
    db.add(db_inventario)
    db.commit()
    db.refresh(db_inventario)
    return {"message": "Inventario creado"}

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



@app.get("/pedidos/{pedido_id}/total")
async def get_total_pedido(pedido_id: int, db: Session = Depends(get_db)):
    total = calcular_total_pedido(pedido_id, db)
    return {"total": total}



@app.post("/detalles_pedidos", status_code=201)
def create_detalle_pedido(detalle_pedido: DetallePedidoCreate, db: Session = Depends(get_db)):
    db_detalle_pedido = DetallePedidoDB(**detalle_pedido.dict())
    db.add(db_detalle_pedido)
    db.commit()
    db.refresh(db_detalle_pedido)
    actualizar_subtotal(db_detalle_pedido.id, db)
    actualizar_total_pedido(db_detalle_pedido.pedido_id, db)
    return {"message": "Detalle de pedido creado"}

@app.post("/detalles_pedidos", status_code=201)
def create_detalle_pedido(detalle_pedido: DetallePedidoCreate, db: Session = Depends(get_db)):
    db_detalle_pedido = DetallePedidoDB(**detalle_pedido.dict())
    db.add(db_detalle_pedido)
    db.commit()
    db.refresh(db_detalle_pedido)
    actualizar_pedido(db_detalle_pedido.id, db)
    return {"message": "Detalle de pedido creado"}

@app.put("/detalles_pedidos/{id}")
def update_detalle_pedido(id: int, detalle_pedido: DetallePedidoCreate, db: Session = Depends(get_db)):
    db_detalle_pedido = db.query(DetallePedidoDB).filter(DetallePedidoDB.id == id).first()
    db_detalle_pedido.pedido_id = detalle_pedido.pedido_id
    db_detalle_pedido.producto_id = detalle_pedido.producto_id
    db_detalle_pedido.cantidad = detalle_pedido.cantidad
    db_detalle_pedido.precio_unitario = detalle_pedido.precio_unitario
    db.commit()
    db.refresh(db_detalle_pedido)
    actualizar_pedido(db_detalle_pedido.id, db)
    return {"message": "Detalle de pedido actualizado"}