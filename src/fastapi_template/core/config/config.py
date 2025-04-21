import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FastAPI App"
    debug: bool = False
    admin_email: str = "admin@example.com"
    items_per_user: int = 50
    ai_url: str
    ai_model: str
    max_file_size_mb: int

    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        env_file_encoding="utf-8"
    )


@lru_cache()
def get_settings():
    return Settings()
