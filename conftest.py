"""pytest fixtures.

pytest-playwright already gives us `page`, `context`, `browser`.
We only add page objects and a logged-in shortcut.
"""

import logging
import subprocess
from pathlib import Path

import allure
import pytest
from playwright.sync_api import BrowserContext, Page

from api.book_store_api import BASE_URL as DEMOQA, BookStoreApi
from data.users import get_user
from helpers.book_user import get_book_user
from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutCompletePage,
    CheckoutInfoPage,
    CheckoutOverviewPage,
)
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

log = logging.getLogger("tests")


def pytest_runtest_logstart(nodeid, location):
    """Mark where each test starts in logs/test_run.log."""
    log.info("===== START %s", nodeid)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """On failure, dump a screenshot + URL into the Allure report."""
    outcome = yield
    report = outcome.get_result()
    # Result line: once per test, or on a setup/teardown error.
    if report.when == "call" or report.outcome != "passed":
        log.info("===== %s %s (%s)", report.outcome.upper(), item.nodeid, report.when)

    if report.when == "teardown":
        _attach_videos(item)
        return

    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("page")
    if page is None:
        return

    allure.attach(
        page.screenshot(full_page=True),
        name="screenshot",
        attachment_type=allure.attachment_type.PNG,
    )
    allure.attach(
        page.url,
        name="page url",
        attachment_type=allure.attachment_type.TEXT,
    )


def _attach_videos(item) -> None:
    """Attach artifacts/<test>/video*.webm to Allure.

    Needs `--video on` or `--video retain-on-failure`.

    pytest-playwright writes the video only after the browser context closes,
    i.e. during teardown — that's why this runs on the teardown report.
    """
    # pytest-playwright's per-test folder; only present for browser tests.
    output_path = (item.funcargs or {}).get("output_path")
    if not output_path:
        return
    for video in sorted(Path(output_path).glob("video*.webm")):
        log.info("Attach video %s", video)
        allure.attach.file(
            str(video), name=video.name, attachment_type=allure.attachment_type.WEBM
        )


def pytest_sessionfinish(session, exitstatus):
    """Build a single-file HTML report.

    file:// cannot load the multi-file Allure SPA.
    """
    root = Path(session.config.rootpath)
    results = root / "allure-results"
    report = root / "reports"
    if not results.exists():
        return

    try:
        subprocess.run(
            [
                "allure",
                "generate",
                str(results),
                "-o",
                str(report),
                "--clean",
                "--single-file",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        print("\nAllure CLI missing — brew install allure")
        return
    except subprocess.CalledProcessError as exc:
        print(f"\nAllure generate failed:\n{exc.stderr}")
        return

    print(f"\nAllure HTML: {report / 'index.html'}")


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_info_page(page: Page) -> CheckoutInfoPage:
    return CheckoutInfoPage(page)


@pytest.fixture
def checkout_overview_page(page: Page) -> CheckoutOverviewPage:
    return CheckoutOverviewPage(page)


@pytest.fixture
def checkout_complete_page(page: Page) -> CheckoutCompletePage:
    return CheckoutCompletePage(page)


@pytest.fixture
def logged_in(login_page: LoginPage, inventory_page: InventoryPage) -> InventoryPage:
    """Most tests start after login. Do that once here, not in every test."""
    login_page.open()
    login_page.login(*get_user("standard"))
    return inventory_page


# ---------- DemoQA Book Store (API + UI) ----------


@pytest.fixture
def book_api() -> BookStoreApi:
    return BookStoreApi()


@pytest.fixture
def book_user(book_api: BookStoreApi):
    """Create + log in a fresh user via API. Delete it afterwards if the test did not.

    Yields {"id", "username", "password"}.
    """
    username, password = get_book_user()

    response = book_api.create_user(username, password)
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["username"] == username
    assert body["books"] == []
    # Swagger says `userId`, the real response says `userID`.
    user_id = body["userID"]

    book_api.login(username, password)
    yield {"id": user_id, "username": username, "password": password}

    # Safety net: a failed test must not leave the user behind.
    if book_api.get_user(user_id).status_code == 200:
        book_api.delete_user(user_id)


@pytest.fixture
def book_store_ui(context: BrowserContext, book_api: BookStoreApi, book_user) -> dict:
    """Log the browser in with the API's token (no login form).

    DemoQA keeps one token per user, so a UI form login would kill the API
    token. Sharing it through the same cookies the site sets keeps both alive.
    """
    cookies = {
        "token": book_api.token,
        "expires": book_api.token_expires,
        "userID": book_user["id"],
        "userName": book_user["username"],
    }
    context.add_cookies(
        [{"name": k, "value": v, "url": DEMOQA} for k, v in cookies.items()]
    )
    return book_user
