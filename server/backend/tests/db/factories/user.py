import random

from factory import LazyFunction

from ....db.models import constants
from ....db.models.user import User
from .base_factory import BaseFactory
from .utils import fake, generate_hex_value


class UserFactory(BaseFactory):
    """
    Create and return User instance or instances.
    """

    username = LazyFunction(
        lambda: "".join(
            fake.random_letters(random.randint(1, constants.MAX_LENGTH_USER_NAME - 1))
        ).lower()
    )
    hashed_password = generate_hex_value(size=8)

    class Meta:
        model = User
