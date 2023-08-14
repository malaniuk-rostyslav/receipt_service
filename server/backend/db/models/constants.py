from enum import Enum

MAX_LENGTH_USER_NAME: int = 256


class PaymentType(str, Enum):
    CASH = "CASH"
    CARD = "CARD"
