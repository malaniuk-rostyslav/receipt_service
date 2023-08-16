from factory import post_generation

from ....db.models import Receipt
from ....db.models.constants import PaymentTypeEnum
from .base_factory import BaseFactory, factory_session


class ReceiptFactory(BaseFactory):
    """
    Create and return Receipt instance or instances.
    """

    payment_type = PaymentTypeEnum.CARD.value
    amount = 30
    total = 40
    rest = 10

    class Meta:
        model = Receipt

    @post_generation
    def unbound_from_session(self, create, extracted, **kwargs):
        factory_session.commit()
        factory_session.refresh(self)
        factory_session.expunge(self)
