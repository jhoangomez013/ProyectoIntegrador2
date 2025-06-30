
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
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

@app.post("/permisos", status_code=201)
def crear_permisos(permiso: PermisoCreate, db: Session = Depends(get_db)):
    db_permiso = models.PermisoDB(**permiso.dict())
    db.add(db_permiso)
    db.commit()
    db.refresh(db_permiso)
    return {"message": "Permiso creado"}

@app.get("/permisos",response_model=list[Permiso])
def get_permisos(db: Session = Depends(get_db)):
    return db.query(models.PermisoDB).all()

@app.get("/permisos/{id}", response_model=Permiso)
def get_permiso(id: int, db: Session = Depends(get_db)):
    return db.query(models.PermisoDB).filter(models.PermisoDB.id == id).first()

@app.put("/permiso/{id}")
def update_permiso(id:int,permiso:Permiso,db: Session = Depends(get_db)):
    db_permiso = db.query(models.PermisoDB).filter(models.PermisoDB.id== id).first()
    if db_permiso is None:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    db_permiso.descripcion= permiso.descripcion
    db_permiso.nombre=permiso.nombre
    db.commit()
    db.refresh(db_permiso)
    return {"message": "Información del Permiso actualizado"}

@app.delete("/permisos/{id}")
def delete_permiso(id: int, db: Session = Depends(get_db)):
    db_permiso = db.query(models.PermisoDB).filter(models.PermisoDB.id == id).first()
    if db_permiso is None:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    db.delete(db_permiso)
    db.commit()
    return {"message": "Permiso eliminado"}
