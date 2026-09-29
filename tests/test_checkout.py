import allure
from playwright.sync_api import expect
from pytest_bdd import scenario

from helpers.customer import get_customer
from tests.cucumber import then, when


@allure.feature("Checkout")
@scenario("features/checkout.feature", "User can buy one item")
def test_user_can_buy_one_item():
    pass


@when("the user opens the cart")
def user_opens_cart(logged_in):
    logged_in.open_cart()


@then("the cart title is {string}")
def cart_title_is(cart_page, string):
    expect(cart_page.page_title).to_have_text(string)


@then("the cart contains {string}")
def cart_contains(cart_page, string):
    assert string in cart_page.item_names_in_cart()


@when("the user starts checkout")
def user_starts_checkout(cart_page):
    cart_page.checkout()


@when("the user enters a new customer")
def user_enters_new_customer(checkout_info_page):
    customer = get_customer()
    checkout_info_page.fill_info(
        customer["first_name"],
        customer["last_name"],
        customer["postal_code"],
    )


@then("the overview title is {string}")
def overview_title_is(checkout_overview_page, string):
    expect(checkout_overview_page.page_title).to_have_text(string)


@then("the order total contains {string}")
def order_total_contains(checkout_overview_page, string):
    expect(checkout_overview_page.total).to_contain_text(string)


@when("the user finishes the order")
def user_finishes_order(checkout_overview_page):
    checkout_overview_page.finish()


@then("the order confirmation is {string}")
def order_confirmation_is(checkout_complete_page, string):
    expect(checkout_complete_page.header).to_have_text(string)
