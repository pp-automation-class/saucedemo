# Sauce Demo — Playwright + pytest POM

KISS test framework for [saucedemo.com](https://www.saucedemo.com/).
Python, UV, Playwright, pytest, Page Object Model, Allure.

## Layout

```
conftest.py              # fixtures + Allure screenshot-on-fail + HTML report
.env / .env.example      # login/password pairs (do not commit .env)
data/users.py            # get_user("standard") -> (login, password)
helpers/customer.py      # Faker: get_customer() -> first / last / ZIP
pages/                   # one class per screen — selectors + actions
tests/                   # what the user does, not how the DOM works
allure-results/          # raw Allure JSON (gitignored)
reports/index.html       # single-file HTML report (gitignored)
logs/test_run.log        # INFO/DEBUG log of the last run (gitignored)
```

Rule: if a selector changes, you edit **one page object**, not every test.

## Setup

```bash
uv sync
cp .env.example .env          # then put real login/password pairs in .env
uv run playwright install chromium
brew install allure           # once — needed to build reports/index.html
```

## Credentials

`.env` — one pair per user, `login/password`. `.env.example` is placeholders only.

```env
STANDARD_USER=login/password
LOCKED_OUT_USER=login/password
```

```python
from data.users import get_user

login, password = get_user("standard")   # or get_user("STANDARD_USER")
login_page.login(*get_user("locked_out"))
```

Checkout identity is fake, not from `.env`:

```python
from helpers.customer import get_customer

customer = get_customer()  # {"first_name", "last_name", "postal_code"}
```

## Run

```bash
uv run pytest
uv run pytest --headed
uv run pytest --headed --slowmo 800
uv run pytest tests/test_login.py
```

## Logs

Every run writes `logs/test_run.log` (gitignored, overwritten each run).
Page objects log user actions at **INFO** (default) and details at **DEBUG**.

```bash
uv run pytest                          # INFO: "Log in as standard_user", "Add to cart: ..."
uv run pytest --log-file-level=DEBUG   # + selectors, cart contents, fake customer
```

In your own code: `log = logging.getLogger(__name__)`, then `log.info(...)` / `log.debug(...)`.
Never log passwords.

## Allure report

Every `uv run pytest` writes `allure-results/`, then builds **one** HTML file:
`reports/index.html` (`--single-file`).

Open that file in a browser. Do **not** use the default multi-file Allure output —
Chrome blocks extra JSON on `file://` and the report stuck on "Loading...".

Failed tests attach a full-page screenshot + URL.

```bash
uv run pytest
open reports/index.html
```

## POM

Tests call `login_page.login(...)`. They never `page.fill("#user-name", ...)`.

Sauce Demo already exposes `data-test` on every important element — use that,
not brittle CSS classes or XPath.
