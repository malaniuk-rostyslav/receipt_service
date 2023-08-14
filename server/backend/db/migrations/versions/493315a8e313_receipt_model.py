"""Receipt model

Revision ID: 493315a8e313
Revises: 0b1bf0b187f5
Create Date: 2023-08-14 21:01:43.170072

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "493315a8e313"
down_revision: Union[str, None] = "0b1bf0b187f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "receipt",
        sa.Column(
            "id", sa.Integer(), autoincrement=True, nullable=False, comment="Unique id"
        ),
        sa.Column(
            "creator_id",
            sa.Integer(),
            nullable=False,
            comment="Receipt created by user id",
        ),
        sa.Column("payment_type", sa.VARCHAR(), nullable=False),
        sa.Column("amount", sa.DECIMAL(), nullable=False, comment="Amount to pay"),
        sa.Column("total", sa.DECIMAL(), nullable=False),
        sa.Column("rest", sa.DECIMAL(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
            comment="Receipt created at",
        ),
        sa.ForeignKeyConstraint(["creator_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_receipt_amount_btree",
        "receipt",
        ["amount"],
        unique=False,
        postgresql_using="btree",
    )
    op.create_index(
        "ix_receipt_created_at_btree",
        "receipt",
        ["created_at"],
        unique=False,
        postgresql_using="btree",
    )
    op.create_index(
        "ix_receipt_id_btree", "receipt", ["id"], unique=False, postgresql_using="btree"
    )
    op.create_index(
        "ix_receipt_payment_type_btree",
        "receipt",
        ["payment_type"],
        unique=False,
        postgresql_using="btree",
    )
    op.create_index(
        "ix_receipt_rest_btree",
        "receipt",
        ["rest"],
        unique=False,
        postgresql_using="btree",
    )
    op.create_index(
        "ix_receipt_total_btree",
        "receipt",
        ["total"],
        unique=False,
        postgresql_using="btree",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        "ix_receipt_total_btree", table_name="receipt", postgresql_using="btree"
    )
    op.drop_index(
        "ix_receipt_rest_btree", table_name="receipt", postgresql_using="btree"
    )
    op.drop_index(
        "ix_receipt_payment_type_btree", table_name="receipt", postgresql_using="btree"
    )
    op.drop_index("ix_receipt_id_btree", table_name="receipt", postgresql_using="btree")
    op.drop_index(
        "ix_receipt_created_at_btree", table_name="receipt", postgresql_using="btree"
    )
    op.drop_index(
        "ix_receipt_amount_btree", table_name="receipt", postgresql_using="btree"
    )
    op.drop_table("receipt")
    # ### end Alembic commands ###
