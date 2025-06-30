from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth import Token, login
from Base_De_Datos.database import get_db
from sqlalchemy.orm import Session

app = APIRouter()

@app.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login(form_data, db)