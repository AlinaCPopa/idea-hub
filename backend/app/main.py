from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routers import health, auth, users, ideas
from .core.config import settings
from .db import init_db as init_db_module

app = FastAPI(title="IdeaHub API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(health.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(ideas.router, prefix="/ideas", tags=["ideas"])

@app.on_event("startup")
def _startup_create_schema():
    """Ensure the database schema exists at startup.

    In local dev you normally run `python -m app.db.init_db` manually. In a
    container (e.g. Azure Container Apps / App Service) that step wasn't being
    executed, so hitting `/ideas` before tables exist caused an OperationalError
    ("no such table: ideas") -> 500 response. This lightweight guard creates
    the tables if they don't exist (idempotent for SQLite & most RDBMS). For a
    production RDBMS replace with migrations (Alembic) instead of metadata.create_all.
    """
    # Only auto-create for simple/dev setups; for Postgres you would remove and use migrations.
    try:
        init_db_module.init_db()
    except Exception as exc:  # pragma: no cover - defensive logging
        # Avoid crashing the app; surface via /health/db instead.
        print(f"[startup] init_db failed: {exc}")

@app.get("/")
def root():
    return {"message": "IdeaHub backend running"}
