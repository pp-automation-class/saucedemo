"""Fake checkout identity. Faker lives here — not in page objects or .env."""

import logging

from faker import Faker

# Faker spams DEBUG with locale lookups — keep our DEBUG log readable.
logging.getLogger("faker").setLevel(logging.INFO)

fake = Faker()


def get_customer() -> dict[str, str]:
    """Fresh name + ZIP each call. Sauce Demo does not validate the values."""
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "postal_code": fake.postcode(),
    }
