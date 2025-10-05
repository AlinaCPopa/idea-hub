from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...db import models
from ...schemas.idea import IdeaCreate, IdeaRead
from ..deps import get_current_user
from typing import List

router = APIRouter()

@router.get("/", response_model=List[IdeaRead])
def list_ideas(db: Session = Depends(get_db)):
    ideas = db.query(models.Idea).all()
    return [IdeaRead.model_validate({
        **i.__dict__,
        "likes": len(i.likes)
    }) for i in ideas]

@router.post("/", response_model=IdeaRead, status_code=status.HTTP_201_CREATED)
def create_idea(payload: IdeaCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    idea = models.Idea(title=payload.title, description=payload.description, owner_id=current_user.id)
    db.add(idea)
    db.commit()
    db.refresh(idea)
    return IdeaRead.model_validate({**idea.__dict__, "likes": 0})

@router.post("/{idea_id}/like", response_model=IdeaRead)
def like_idea(idea_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    idea = db.query(models.Idea).filter(models.Idea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    existing = db.query(models.Like).filter(models.Like.idea_id == idea_id, models.Like.user_id == current_user.id).first()
    if existing:
        return IdeaRead.model_validate({**idea.__dict__, "likes": len(idea.likes)})
    like = models.Like(idea_id=idea_id, user_id=current_user.id)
    db.add(like)
    db.commit()
    db.refresh(idea)
    return IdeaRead.model_validate({**idea.__dict__, "likes": len(idea.likes)})
