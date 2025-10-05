from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from .session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ideas = relationship("Idea", back_populates="owner")
    likes = relationship("Like", back_populates="user")

class Idea(Base):
    __tablename__ = "ideas"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False)
    description = Column(String(500))
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    likes = relationship("Like", back_populates="idea")
    owner = relationship("User", back_populates="ideas")

class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    idea_id = Column(Integer, ForeignKey("ideas.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="likes")
    idea = relationship("Idea", back_populates="likes")
    __table_args__ = (UniqueConstraint('user_id', 'idea_id', name='uq_user_idea'),)
