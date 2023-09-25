from sqlalchemy import Column, DateTime, Index, Integer, String, func

from ..base import Base
from .constants import MAX_LENGTH_USER_NAME


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Unique id")
    username = Column(
        String(MAX_LENGTH_USER_NAME),
        nullable=False,
        unique=True,
        comment="Unique username",
    )
    hashed_password = Column(String, nullable=False, comment="Hashed password")
    created_at = Column(
        DateTime(timezone=False),
        default=func.now(),
        server_default=func.now(),
        comment="User created at",
    )

    _table_args_ = (
        Index(
            "ix_user_username_btree", username, unique=True, postgresql_using="btree"
        ),
        Index("ix_user_created_at_btree", created_at, postgresql_using="btree"),
    )
