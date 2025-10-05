from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...db import models
from ...core.security import verify_password, create_access_token

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token(subject=user.username)
    return {"access_token": token, "token_type": "bearer"}
