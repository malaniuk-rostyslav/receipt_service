from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....db import models
from ...core.deps import get_db
from ...core.security import (AuthRequestForm, create_access_token,
                              verify_password)
from ...schemas.token import Token

router = APIRouter()


async def authenticate(
    db: Session, username: str, password: str
) -> Optional[models.User]:
    user = db.query(models.User).filter_by(username=username).one_or_none()
    if not user:
        return None
    valid_password = verify_password(password, user.hashed_password)
    if not valid_password:
        return None
    return user


@router.post("/access-token", status_code=status.HTTP_200_OK, response_model=Token)
async def obtain_access_token(
    db: Session = Depends(get_db), form_data: AuthRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    FORM data: \n
    `username`: str \n
    `password`: str \n
    Responses: \n
    `201` Created \n
    `401` Unauthorized - Returns if User not found \n
    """

    user = await authenticate(
        db, form_data.username, form_data.password.get_secret_value()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    access_token = create_access_token(user.username)
    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }
