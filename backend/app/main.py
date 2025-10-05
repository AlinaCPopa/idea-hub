from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routers import health, auth, users, ideas
from .core.config import settings

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

@app.get("/")
def root():
    return {"message": "IdeaHub backend running"}
