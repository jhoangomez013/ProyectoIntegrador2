
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import SessionLocal
import models 
from schemas import *
from sqlalchemy.orm import Session 
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from auth import get_current_user
from services import tiene_permiso

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

app = APIRouter()
templates = Jinja2Templates(directory="templates")
# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Endpoint Usuarios

@app.get("/usuarios/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    current_user = await get_current_user(token)
    # Lógica para obtener información del usuario autenticado
    return {"message": f"Hola, {current_user.username}"}

#@app.get("/usuarios", response_model=List[Usuario])
#def get_usuarios(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
#    current_user = get_current_user(token, db)
#    return db.query(models.UsuarioDB).all()
@app.get("/usuarios", response_model=List[Usuario])
def get_usuarios(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token, db)
    permiso = db.query(models.PermisoDB).filter(models.PermisoDB.nombre == "ver_usuarios").first()
    if not permiso:
        raise HTTPException(status_code=500, detail="Permiso no encontrado")
    if not tiene_permiso(current_user.id, permiso.id, db):
        raise HTTPException(status_code=403, detail="No tienes permiso para ver la lista de usuarios")
    return db.query(models.UsuarioDB).all()


@app.post("/usuarios", status_code=201)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(usuario.password)
    db_usuario = models.UsuarioDB(**usuario.dict(exclude={"password"}), password=hashed_password)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return {"message": "Usuario creado", "id": db_usuario.id}

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