from pydantic import BaseModel
from datetime import datetime

class IdeaBase(BaseModel):
    title: str
    description: str | None = None

class IdeaCreate(IdeaBase):
    pass

class IdeaRead(IdeaBase):
    id: int
    owner_id: int | None = None
    likes: int = 0
    created_at: datetime | None = None

    class Config:
        from_attributes = True
