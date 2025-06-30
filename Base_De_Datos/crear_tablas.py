from database import engine
from models import Base

def crear_tablas():
    Base.metadata.create_all(engine)
    print("Tablas creadas con éxito")

crear_tablas()