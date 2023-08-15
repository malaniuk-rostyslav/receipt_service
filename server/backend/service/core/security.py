from datetime import datetime, timedelta
from typing import Any, Union

from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from pydantic import SecretStr

from .settings import settings

pwd_contex = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_contex.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_contex.verify(password, hash)


class AuthRequestForm(OAuth2PasswordRequestForm):
    def __init__(
        self,
        username: str = Form(default=...),
        password: SecretStr = Form(default=...),
    ):
        self.username = username
        self.password = password


def create_access_token(subject: Union[str, Any], exp_delta: timedelta = None) -> str:
    """
    Create access JWT token for login into the system
    """
    expire = datetime.utcnow() + timedelta(
        minutes=exp_delta
        if exp_delta
        else settings.ACCESS_TOKEN_EXPIRE_MINUTES  # type:ignore
    )
    to_encode = {
        "exp": expire,
        "sub": str(subject),
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
