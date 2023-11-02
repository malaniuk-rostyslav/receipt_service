from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ...db import models
from ...db.session import SessionLocal
from ..core.settings import settings
from ..schemas.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/access-token")


async def get_db() -> Generator:
    with SessionLocal() as db:
        yield db


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(sub=payload["sub"])
    except (jwt.JWTError, ValidationError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    user = (
        db.query(models.User)
        .filter(models.User.username == token_data.sub)
        .one_or_none()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user
