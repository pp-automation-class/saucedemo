import logging

from playwright.sync_api import Page

from pages.base_page import BasePage

log = logging.getLogger(__name__)


class InventoryPage(BasePage):
    """https://www.saucedemo.com/inventory.html — product catalog."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.item_names = page.locator("[data-test='inventory-item-name']")
        self.sort = page.locator("[data-test='product-sort-container']")

    def add_to_cart(self, product_name: str) -> None:
        """Sauce builds data-test from the product name.

        'Sauce Labs Backpack' -> [data-test='add-to-cart-sauce-labs-backpack']
        """
        slug = product_name.lower().replace(" ", "-")
        log.info("Add to cart: %s", product_name)
        self.click(self.page.locator(f"[data-test='add-to-cart-{slug}']"))

    def remove_from_cart(self, product_name: str) -> None:
        slug = product_name.lower().replace(" ", "-")
        log.info("Remove from cart: %s", product_name)
        self.click(self.page.locator(f"[data-test='remove-{slug}']"))

    def product_names(self) -> list[str]:
        names = self.item_names.all_inner_texts()
        log.debug("Catalog: %s", names)
        return names

    def sort_by(self, value: str) -> None:
        # Option values: az | za | lohi | hilo
        log.info("Sort by %s", value)
        self.select(self.sort, value)
