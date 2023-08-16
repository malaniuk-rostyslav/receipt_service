from sqlalchemy import (DECIMAL, Column, DateTime, ForeignKey, Index, Integer,
                        String, func)
from sqlalchemy.orm import relationship

from ..base import Base
from .receipt import association_receipt_product_table


class Product(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Unique id")
    creator_id = Column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        comment="Product created by user id",
    )
    name = Column(
        String,
        unique=True,
        doc="Product's name",
        nullable=False,
    )
    price = Column(
        DECIMAL,
        doc="Product's price",
        nullable=False,
    )
    receipts = relationship(
        "Receipt",
        secondary=association_receipt_product_table,
        lazy="noload",
    )
    created_at = Column(
        DateTime(timezone=False),
        default=func.now(),
        server_default=func.now(),
        comment="Receipt created at",
    )
    _table_args_ = (
        Index("ix_product_id_btree", id, postgresql_using="btree"),
        Index("ix_product_name_btree", name, postgresql_using="btree"),
        Index("ix_product_price_btree", price, postgresql_using="btree"),
        Index("ix_product_created_at_btree", created_at, postgresql_using="btree"),
    )
