from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...db import models
from ...core.security import hash_password
from ...schemas.user import UserCreate, UserRead
from ..deps import get_current_user
from typing import List

router = APIRouter()

@router.get("/", response_model=List[UserRead])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(new_user: UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == new_user.username).first():
        raise HTTPException(status_code=400, detail="Username taken")
    user = models.User(username=new_user.username, hashed_password=hash_password(new_user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/me", response_model=UserRead)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user
