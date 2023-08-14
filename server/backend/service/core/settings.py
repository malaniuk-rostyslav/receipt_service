from typing import Optional

from pydantic_settings import BaseSettings


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

    class Config:
        case_sensitive = True


settings = Settings()
