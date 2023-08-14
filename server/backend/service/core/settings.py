from typing import Any, Dict, Optional

from pydantic import validator
from pydantic_settings import BaseSettings

from .validators import PostgresDsn


class Settings(BaseSettings):
    PROJECT_NAME: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CONFIRM_ACCOUNT_TOKEN_EXPIRE_MINUTES: int = 10
    CONFIRM_ACCOUNT_TOKEN_EXPIRE_SECONDS: Optional[int] = None
    RESET_PASSWORD_TOKEN_EXPIRE_MINUTES: int = 10
    RESET_PASSWORD_TOKEN_EXPIRE_SECONDS: Optional[int] = None
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            # user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True


settings = Settings()
