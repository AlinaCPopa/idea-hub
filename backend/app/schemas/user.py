from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True
