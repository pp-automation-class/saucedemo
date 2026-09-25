"""pytest fixtures.

pytest-playwright already gives us `page`, `context`, `browser`.
We only add page objects and a logged-in shortcut.
"""

import logging
import subprocess
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from data.users import get_user
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
