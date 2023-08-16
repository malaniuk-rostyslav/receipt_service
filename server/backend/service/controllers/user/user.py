from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....db import models
from ...core.deps import get_db
from ...core.security import hash_password
from ...schemas.user import User as UserSchema
from ...schemas.user import UserCreate

router = APIRouter()


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserSchema
)
def register_user(form_data: UserCreate, db: Session = Depends(get_db)) -> Any:
    """
    Register user \n
    JSON data: \n
    `username`: str \n
    `password`: str \n
    `password_confirm`: str \n
    Responses: \n
    `201` Created \n
    `400` Bad Request - Returns if User with such username already exists \n
    `422` Unprocessable Entity - Returns if wrong form_data field
    """
    username_exists = db.query(
        db.query(models.User)
        .filter(models.User.username == form_data.username)
        .exists()
    ).scalar()
    if username_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with such username already exists",
        )
    form_data.__dict__.update(
        {
            "hashed_password": hash_password(form_data.hashed_password),
        }
    )
    user = models.User(
        username=form_data.username, hashed_password=form_data.hashed_password
    )
    db.add(user)
    db.commit()
    return user
