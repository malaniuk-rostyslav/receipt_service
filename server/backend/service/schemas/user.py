from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator


class UserCreate(BaseModel):
    username: str
    password: str
    hashed_password: str = Field(alias="password_confirm")

    @validator("hashed_password")
    def validate_passwords(cls, value, values):
        if value != values.get("password"):
            raise ValueError("Passwords missmatch")
        return value


class User(BaseModel):
    id: PositiveInt
    username: Optional[str]

    class Config:
        orm_mode = True
