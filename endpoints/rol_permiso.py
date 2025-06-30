
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from Base_De_Datos.database import SessionLocal
from Base_De_Datos import models 
from schemas import *
from sqlalchemy.orm import Session 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = APIRouter()
templates = Jinja2Templates(directory="templates")
# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Endpoint Rol_Permiso
@app.post("/roles/{rol_id}/permisos/{permiso_id}")
def agregar_permiso_a_rol(rol_id: int, permiso_id: int, db: Session = Depends(get_db)):
    rol = db.query(models.RolDB).filter(models.RolDB.id == rol_id).first()
    permiso = db.query(models.PermisoDB).filter(models.PermisoDB.id == permiso_id).first()
    if not rol or not permiso:
        raise HTTPException(status_code=404, detail="Rol o permiso no encontrado")
    rol_permiso = models.RolPermisoDB(rol_id=rol_id, permiso_id=permiso_id)
    db.add(rol_permiso)
    db.commit()
    db.refresh(rol_permiso)
    return {"message": "Permiso asignado al rol"}

@app.get("/roles/{rol_id}/permisos")
def obtener_permisos_de_rol(rol_id: int, db: Session = Depends(get_db)):
    rol = db.query(models.RolDB).filter(models.RolDB.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    permisos = db.query(models.RolPermisoDB).filter(models.RolPermisoDB.rol_id == rol_id).all()
    return [{"permiso_id": permiso.permiso_id} for permiso in permisos]

@app.put("/roles/{rol_id}/permisos/{permiso_id}")
def actualizar_permiso_de_rol(rol_id: int, permiso_id: int, nuevo_permiso_id: int, db: Session = Depends(get_db)):
    rol = db.query(models.RolDB).filter(models.RolDB.id == rol_id).first()
    permiso = db.query(models.PermisoDB).filter(models.PermisoDB.id == permiso_id).first()
    nuevo_permiso = db.query(models.PermisoDB).filter(models.PermisoDB.id == nuevo_permiso_id).first()
    if not rol or not permiso or not nuevo_permiso:
        raise HTTPException(status_code=404, detail="Rol o permiso no encontrado")
    rol_permiso = db.query(models.RolPermisoDB).filter(models.RolPermisoDB.rol_id == rol_id, models.RolPermisoDB.permiso_id == permiso_id).first()
    if not rol_permiso:
        raise HTTPException(status_code=404, detail="Permiso no asignado al rol")
    rol_permiso.permiso_id = nuevo_permiso_id
    db.commit()
    db.refresh(rol_permiso)
    return {"message": "Permiso actualizado"}

@app.delete("/roles/{rol_id}/permisos/{permiso_id}")
def eliminar_permiso_de_rol(rol_id: int, permiso_id: int, db: Session = Depends(get_db)):
    rol = db.query(models.RolDB).filter(models.RolDB.id == rol_id).first()
    permiso = db.query(models.PermisoDB).filter(models.PermisoDB.id == permiso_id).first()
    if not rol or not permiso:
        raise HTTPException(status_code=404, detail="Rol o permiso no encontrado")
    rol_permiso = db.query(models.RolPermisoDB).filter(models.RolPermisoDB.rol_id == rol_id, models.RolPermisoDB.permiso_id == permiso_id).first()
    if not rol_permiso:
        raise HTTPException(status_code=404, detail="Permiso no asignado al rol")
    db.delete(rol_permiso)
    db.commit()
    return {"message": "Permiso eliminado del rol"}