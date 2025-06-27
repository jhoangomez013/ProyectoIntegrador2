from pydantic import BaseModel
from pydantic import BaseModel
from typing import List
import datetime

# Modelo de datos
class ProductoCreate(BaseModel):
    nombre: str
    descripcion: str
    precio: float

class Producto(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float

    class Config:
        from_attributes = True

class PedidoCreate(BaseModel):
    fecha: datetime.datetime
    total: float
    usuario_id: int

class Pedido(BaseModel):
    id: int
    fecha: datetime.datetime
    total: float
    usuario_id: int

    class Config:
        from_attributes = True

class AnotacionCreate(BaseModel):
    pedido_id: int
    texto: str

class Anotacion(BaseModel):
    id: int
    pedido_id: int
    texto: str

    class Config:
        from_attributes = True

class PedidoConAnotaciones(BaseModel):
    id: int
    fecha: datetime.datetime
    total: float
    usuario_id: int
    anotaciones: List[Anotacion] 

    class Config:
        from_attributes = True

class UsuarioCreate(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str
    rol_id: int

class Usuario(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    password: str
    rol_id: int

    class Config:
        from_attributes = True

class InventarioCreate(BaseModel):
    producto_id: int
    cantidad: int

class Inventario(BaseModel):
    id: int
    producto_id: int
    cantidad: int

    class Config:
        from_attributes = True

class RolCreate(BaseModel):
    nombre: str
    descripcion: str

class Rol(BaseModel):
    id: int
    nombre: str
    descripcion: str

    class Config:
        from_attributes = True

class PermisoCreate(BaseModel):
    nombre: str
    descripcion: str

class Permiso(BaseModel):
    id: int
    nombre: str
    descripcion: str

    class Config:
        from_attributes = True

class RolPermisoCreate(BaseModel):
    rol_id: int
    permiso_id: int

class RolPermiso(BaseModel):
    id: int
    rol_id: int
    permiso_id: int

    class Config:
        from_attributes = True

class DetallePedidoCreate(BaseModel):
    pedido_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float

class DetallePedido(BaseModel):
    id: int
    pedido_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float

    class Config:
        from_attributes = True