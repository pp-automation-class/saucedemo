"""Fresh DemoQA Book Store credentials. Faker lives here, not in tests."""

from uuid import uuid4

from faker import Faker

fake = Faker()


def get_book_user() -> tuple[str, str]:
    """Unique username + a password that passes DemoQA's rules.

    Rules: 8+ chars, upper, lower, digit and a special character.
    """
    username = f"qa_{uuid4().hex[:10]}"
    # Faker's special chars include ()_+ which DemoQA rejects, so add our own.
    password = fake.password(length=11, special_chars=False) + fake.random_element(
        "!@#$%^&*"
    )
    return username, password
