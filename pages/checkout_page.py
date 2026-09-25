import logging

from playwright.sync_api import Page

from pages.base_page import BasePage

log = logging.getLogger(__name__)

# Three screens, one file — they are one linear flow, not three features.


class CheckoutInfoPage(BasePage):
    """https://www.saucedemo.com/checkout-step-one.html"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.first_name = page.locator("[data-test='firstName']")
        self.last_name = page.locator("[data-test='lastName']")
        self.postal_code = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.error = page.locator("[data-test='error']")

    def fill_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        log.info("Fill checkout info")
        log.debug("Customer: %s %s, %s", first_name, last_name, postal_code)
        self.fill(self.first_name, first_name)
        self.fill(self.last_name, last_name)
        self.fill(self.postal_code, postal_code)
        self.click(self.continue_button)


class CheckoutOverviewPage(BasePage):
    """https://www.saucedemo.com/checkout-step-two.html"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.item_names = page.locator("[data-test='inventory-item-name']")
        self.subtotal = page.locator("[data-test='subtotal-label']")
        self.tax = page.locator("[data-test='tax-label']")
        self.total = page.locator("[data-test='total-label']")
        self.finish_button = page.locator("[data-test='finish']")

    def finish(self) -> None:
        log.info("Finish order")
        self.click(self.finish_button)


class CheckoutCompletePage(BasePage):
    """https://www.saucedemo.com/checkout-complete.html"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.header = page.locator("[data-test='complete-header']")
        self.back_home = page.locator("[data-test='back-to-products']")
