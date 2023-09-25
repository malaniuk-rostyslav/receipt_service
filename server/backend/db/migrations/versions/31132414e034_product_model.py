"""Product model

Revision ID: 31132414e034
Revises: 99d17ced5690
Create Date: 2023-08-16 08:02:19.696051

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "31132414e034"
down_revision: Union[str, None] = "99d17ced5690"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "product",
        sa.Column(
            "id", sa.Integer(), autoincrement=True, nullable=False, comment="Unique id"
        ),
        sa.Column(
            "creator_id",
            sa.Integer(),
            nullable=False,
            comment="Product created by user id",
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("price", sa.DECIMAL(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
            comment="Receipt created at",
        ),
        sa.ForeignKeyConstraint(["creator_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(
        "ix_product_created_at_btree",
        "product",
        ["created_at"],
        unique=False,
        postgresql_using="btree",
    )
    op.create_index(
        "ix_product_name_btree",
        "product",
        ["name"],
        unique=False,
        postgresql_using="btree",
    )
    op.create_index(
        "ix_product_price_btree",
        "product",
        ["price"],
        unique=False,
        postgresql_using="btree",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        "ix_product_price_btree", table_name="product", postgresql_using="btree"
    )
    op.drop_index(
        "ix_product_name_btree", table_name="product", postgresql_using="btree"
    )
    op.drop_index(
        "ix_product_created_at_btree", table_name="product", postgresql_using="btree"
    )
    op.drop_table("product")
    # ### end Alembic commands ###
