import logging

from playwright.sync_api import Locator, Page

log = logging.getLogger(__name__)


def _selector(locator: Locator) -> str:
    """Playwright's locator string — what you'd type in the POM."""
    impl = getattr(locator, "_impl_obj", None)
    return getattr(impl, "_selector", None) or str(locator)


class BasePage:
    """Shared bits that show up on every logged-in screen (header, cart).

    Keep this tiny. If only one page uses a locator, put it on that page.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        # Sauce Demo uses data-test, not data-testid. Use the attribute as-is.
        self.cart_link = page.locator("[data-test='shopping-cart-link']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")
        self.page_title = page.locator("[data-test='title']")
        self.menu_button = page.locator("[data-test='open-menu']")
        self.logout_link = page.locator("[data-test='logout-sidebar-link']")

    def click(self, locator: Locator) -> None:
        log.debug("Click %s", _selector(locator))
        locator.click()

    def fill(self, locator: Locator, value: str) -> None:
        # Locator only — never the value (passwords go through here).
        log.debug("Fill %s", _selector(locator))
        locator.fill(value)

    def select(self, locator: Locator, value: str) -> None:
        log.debug("Select %s = %s", _selector(locator), value)
        locator.select_option(value)

    def open(self, path: str = "/") -> None:
        # --base-url is set in pyproject.toml, so "/" is the login page.
        log.info("Open %s", path)
        self.page.goto(path)

    def cart_count(self) -> int:
        """Badge is missing when the cart is empty — that's a 0, not a failure."""
        log.debug("Read %s", _selector(self.cart_badge))
        if self.cart_badge.count() == 0:
            log.debug("Cart badge missing -> 0 items")
            return 0
        count = int(self.cart_badge.inner_text())
        log.debug("Cart badge shows %d", count)
        return count

    def open_cart(self) -> None:
        log.info("Open cart")
        self.click(self.cart_link)

    def logout(self) -> None:
        log.info("Log out")
        self.click(self.menu_button)
        self.click(self.logout_link)
