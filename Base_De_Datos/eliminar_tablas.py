from database import engine
from models import Base

def eliminar_tablas():
    Base.metadata.drop_all(engine)
    print("Tablas eliminadas con éxito")

eliminar_tablas()