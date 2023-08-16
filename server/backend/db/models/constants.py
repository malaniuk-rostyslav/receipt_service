from enum import Enum

MAX_LENGTH_USER_NAME: int = 256


class PaymentTypeEnum(str, Enum):
    CASH = "Cash"
    CARD = "Card"
