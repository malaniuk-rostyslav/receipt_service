from sqlalchemy import (DECIMAL, VARCHAR, Column, DateTime, ForeignKey, Index,
                        Integer, func)

from ..base import Base
from .constants import PaymentTypeEnum


class Receipt(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Unique id")
    creator_id = Column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        comment="Receipt created by user id",
    )
    payment_type = Column(
        VARCHAR,
        default=PaymentTypeEnum.CASH,
        doc="Payment type",
        nullable=False,
    )
    amount = Column(DECIMAL, nullable=False, comment="Amount to pay")
    total = Column(
        DECIMAL,
        doc="Total amount paid",
        nullable=False,
    )
    rest = Column(
        DECIMAL,
        doc="Rest to return to customer",
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=False),
        default=func.now(),
        server_default=func.now(),
        comment="Receipt created at",
    )
    _table_args_ = (
        Index("ix_receipt_payment_type_btree", payment_type, postgresql_using="btree"),
        Index("ix_receipt_amount_btree", amount, postgresql_using="btree"),
        Index("ix_receipt_total_btree", total, postgresql_using="btree"),
        Index("ix_receipt_rest_btree", rest, postgresql_using="btree"),
        Index("ix_receipt_created_at_btree", created_at, postgresql_using="btree"),
    )


class ReceiptHistory(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Unique id")
    receipt_id = Column(
        ForeignKey("receipt.id", ondelete="CASCADE"),
        nullable=False,
        comment="Receipt id",
    )
    product_id = Column(
        ForeignKey("product.id", ondelete="CASCADE"),
        nullable=False,
        comment="Product id",
    )
    price = Column(
        DECIMAL,
        doc="Product's price",
        nullable=False,
    )
    quantity = Column(
        Integer,
        doc="Product's quantity",
        nullable=False,
    )
    total = Column(
        DECIMAL,
        doc="Total amount to pay",
        nullable=False,
    )
    _table_args_ = (
        Index("ix_receipt_history_price_btree", price, postgresql_using="btree"),
        Index("ix_receipt_history_quantity_btree", quantity, postgresql_using="btree"),
        Index("ix_receipt_history_total_btree", total, postgresql_using="btree"),
    )
