
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import SessionLocal
import models 
from schemas import *
from sqlalchemy.orm import Session 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = APIRouter()

# Endpoint Rol

@app.get("/roles")
def obtener_roles(db: Session = Depends(get_db)):
    roles = db.query(models.RolDB).all()
    return [{"id": rol.id, "nombre": rol.nombre, "descripcion": rol.descripcion} for rol in roles]

@app.get("/roles/{rol_id}")
def obtener_rol(rol_id: int, db: Session = Depends(get_db)):
    rol = db.query(models.RolDB).filter(models.RolDB.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"id": rol.id, "nombre": rol.nombre, "descripcion": rol.descripcion}

@app.post("/roles")
def crear_rol(rol: RolCreate, db: Session = Depends(get_db)):
    db_rol = db.query(models.RolDB).filter(models.RolDB.nombre == rol.nombre).first()
    if db_rol:
        raise HTTPException(status_code=400, detail="Rol ya existe")
    nuevo_rol = models.RolDB(nombre=rol.nombre, descripcion=rol.descripcion)
    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)
    return {"message": "Rol creado"}

@app.put("/roles/{rol_id}")
def actualizar_rol(rol_id: int, rol: RolCreate, db: Session = Depends(get_db)):
    db_rol = db.query(models.RolDB).filter(models.RolDB.id == rol_id).first()
    if not db_rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db_rol.nombre = rol.nombre
    db_rol.descripcion = rol.descripcion
    db.commit()
    db.refresh(db_rol)
    return {"message": "Rol actualizado"}

@app.delete("/roles/{rol_id}")
def eliminar_rol(rol_id: int, db: Session = Depends(get_db)):
    rol = db.query(models.RolDB).filter(models.RolDB.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    # Eliminar permisos asignados al rol
    db.query(models.RolPermisoDB).filter(models.RolPermisoDB.rol_id == rol_id).delete()
    db.delete(rol)
    db.commit()
    return {"message": "Rol eliminado"}