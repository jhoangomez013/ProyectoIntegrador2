from sqlalchemy import create_engine

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/restapos"

# Crear el motor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

try:
    # Intentar conectar a la base de datos
    connection = engine.connect()
    print("Conexión exitosa")
except Exception as e:
    print("Error al conectar a la base de datos:", str(e))