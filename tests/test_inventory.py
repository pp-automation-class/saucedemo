import allure
from playwright.sync_api import expect

from data.users import BACKPACK


@allure.feature("Inventory")
def test_catalog_lists_products(logged_in):
    names = logged_in.product_names()

    assert BACKPACK in names
    assert len(names) == 6


@allure.feature("Inventory")
def test_add_to_cart_updates_badge(logged_in):
    assert logged_in.cart_count() == 0

    logged_in.add_to_cart(BACKPACK)

    expect(logged_in.cart_badge).to_have_text("1")
