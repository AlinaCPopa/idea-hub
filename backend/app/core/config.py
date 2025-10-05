from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    app_name: str = "IdeaHub"
    jwt_secret: str = "CHANGE_ME_SECRET"  # replace in production
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = "sqlite:///./dev.db"
    # Comma separated CORS origins, e.g. "http://localhost:5173,https://idea-hub.azurewebsites.net"
    cors_origins: List[str] = ["http://localhost:5173"]

    def model_post_init(self, __context):  # type: ignore[override]
        # Support comma separated string in env var
        if isinstance(self.cors_origins, str):  # type: ignore
            raw = self.cors_origins  # type: ignore
            self.cors_origins = [o.strip() for o in raw.split(",") if o.strip()]  # type: ignore

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
