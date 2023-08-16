from ....db.models import Product
from .base_factory import BaseFactory
from .utils import fake


class ProductFactory(BaseFactory):
    """
    Create and return Product instance or instances.
    """

    name = fake.word()
    price = 10

    class Meta:
        model = Product
