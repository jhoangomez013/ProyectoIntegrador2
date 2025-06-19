from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ProductoDB(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)
    precio = Column(Float)

class PedidoDB(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime)
    total = Column(Float)

class AnotacionDB(Base):
    __tablename__ = "anotaciones"

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    texto = Column(String)

class AnexoDB(Base):
    __tablename__ = "anexos"

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    archivo = Column(String)

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    password = Column(String)

class InventarioDB(Base):
    __tablename__ = "inventarios"

    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)
