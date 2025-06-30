from datetime import datetime
from sqlalchemy import Column, Integer, Numeric, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class ProductoDB(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    descripcion = Column(String)
    precio = Column(Numeric(10, 2))

    inventarios = relationship("InventarioDB", backref="producto_inventario")

class PedidoDB(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    total = Column(Numeric(10, 2))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    usuario = relationship("UsuarioDB", backref="pedidos")

class AnotacionDB(Base):
    __tablename__ = "anotaciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    texto = Column(String)

    pedido = relationship("PedidoDB", backref="anotaciones")



class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    password = Column(String)
    rol_id = Column(Integer, ForeignKey("roles.id"))

    rol = relationship("RolDB", backref="usuarios")

class InventarioDB(Base):
    __tablename__ = "inventarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)

class RolDB(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    descripcion = Column(String)

class PermisoDB(Base):
    __tablename__ = "permisos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    descripcion = Column(String)

class RolPermisoDB(Base):
    __tablename__ = "roles_permisos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rol_id = Column(Integer, ForeignKey("roles.id"))
    permiso_id = Column(Integer, ForeignKey("permisos.id"))

    rol = relationship("RolDB", backref="roles_permisos")
    permiso = relationship("PermisoDB", backref="roles_permisos")

class DetallePedidoDB(Base):
    __tablename__ = "detalles_pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)
    precio_unitario = Column(Numeric(10, 2))
    subtotal = Column(Numeric(10, 2))

    pedido = relationship("PedidoDB", backref="detalles_pedidos")
    producto = relationship("ProductoDB", backref="detalles_pedidos")