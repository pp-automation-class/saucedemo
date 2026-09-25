import logging

from playwright.sync_api import Page

from pages.base_page import BasePage

log = logging.getLogger(__name__)


class CartPage(BasePage):
    """https://www.saucedemo.com/cart.html"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.item_names = page.locator("[data-test='inventory-item-name']")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.continue_shopping = page.locator("[data-test='continue-shopping']")

    def item_names_in_cart(self) -> list[str]:
        names = self.item_names.all_inner_texts()
        log.debug("Cart: %s", names)
        return names

    def checkout(self) -> None:
        log.info("Start checkout")
        self.click(self.checkout_button)
