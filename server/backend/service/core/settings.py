import os
from typing import Any, Dict, Optional

from pydantic import validator
from pydantic_settings import BaseSettings

from .validators import PostgresDsn


class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: str = os.getenv("BACKEND_CORS_ORIGINS")

    # Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_PORT: str
    POSTGRES_SERVER: str
    API_V1_STR: str = "/"
    PROJECT_NAME: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True


settings = Settings()
