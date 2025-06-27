from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/restapos"

# Crear el motor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear una base para los modelos
Base = declarative_base()