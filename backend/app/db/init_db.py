from sqlalchemy.orm import Session
from .session import engine, Base, SessionLocal
from .models import User, Idea
from ..core.security import hash_password

def init_db():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        # seed if empty
        if not db.query(User).first():
            try:
                user = User(username="demo", hashed_password=hash_password("demo"))
                db.add(user)
                db.flush()
                idea1 = Idea(title="First Idea", description="An awesome concept", owner_id=user.id)
                idea2 = Idea(title="Second Idea", description="Another innovation", owner_id=user.id)
                db.add_all([idea1, idea2])
                db.commit()
            except Exception as exc:  # pragma: no cover - defensive
                db.rollback()
                print(f"[init_db] Seed failed: {exc}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
