import random

from faker import Factory

fake = Factory.create()


def generate_hex_value(size):
    """
    Generate and return Hex string.
    """
    values_list = list(map(str, range(0, 10))) + list(set(fake.random_letters(9)))
    random_value_list = [random.choice(values_list) for _ in range(size)]
    hex_str = f"0x{''.join(random_value_list)}"
    return hex_str
