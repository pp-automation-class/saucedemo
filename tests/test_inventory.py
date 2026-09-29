import allure
from playwright.sync_api import expect
from pytest_bdd import scenario

from tests.cucumber import then


@allure.feature("Inventory")
@scenario("features/inventory.feature", "Catalog lists products")
def test_catalog_lists_products():
    pass


@allure.feature("Inventory")
@scenario("features/inventory.feature", "Add to cart updates the badge")
def test_add_to_cart_updates_badge():
    pass


@then("the catalog contains {string}")
def catalog_contains(logged_in, string):
    assert string in logged_in.product_names()


@then("the catalog has {int} products")
def catalog_has_products(logged_in, int):
    assert len(logged_in.product_names()) == int


@then("the cart has {int} items")
def cart_has_items(logged_in, int):
    assert logged_in.cart_count() == int


@then("the cart badge shows {string}")
def cart_badge_shows(logged_in, string):
    expect(logged_in.cart_badge).to_have_text(string)
