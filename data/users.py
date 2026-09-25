"""Users + catalog data.

Credentials live in `.env` as `login/password` pairs. This module only *reads* them.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# data/users.py -> project root, so it works no matter where pytest is launched.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

BACKPACK = "Sauce Labs Backpack"


def get_user(role: str) -> tuple[str, str]:
    """Return `(login, password)` from `.env`.

    STANDARD_USER=standard_user/secret_sauce
    get_user("standard")      -> ("standard_user", "secret_sauce")
    get_user("STANDARD_USER") -> same
    """
    key = role.strip().upper()
    if not key.endswith("_USER"):
        key = f"{key}_USER"

    raw = os.getenv(key, "")
    if "/" not in raw:
        raise KeyError(f"{key} must be login/password in .env, got {raw!r}")

    login, password = raw.split("/", 1)
    return login, password
