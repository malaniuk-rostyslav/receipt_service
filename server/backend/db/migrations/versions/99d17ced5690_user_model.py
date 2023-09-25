"""User model

Revision ID: 99d17ced5690
Revises: 
Create Date: 2023-08-14 20:53:43.036946

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "99d17ced5690"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column(
            "id", sa.Integer(), autoincrement=True, nullable=False, comment="Unique id"
        ),
        sa.Column(
            "username",
            sa.String(length=256),
            nullable=False,
            comment="Unique username",
        ),
        sa.Column(
            "hashed_password", sa.String(), nullable=False, comment="Hashed password"
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
            comment="User created at",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(
        "ix_user_created_at_btree",
        "user",
        ["created_at"],
        unique=False,
        postgresql_using="btree",
    )
    op.create_index(
        "ix_user_username_btree",
        "user",
        ["username"],
        unique=True,
        postgresql_using="btree",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_user_username_btree", table_name="user", postgresql_using="btree")
    op.drop_index(
        "ix_user_created_at_btree", table_name="user", postgresql_using="btree"
    )
    op.drop_table("user")
    # ### end Alembic commands ###
