import allure
from playwright.sync_api import expect

from data.users import BACKPACK
from helpers.customer import get_customer


@allure.feature("Checkout")
def test_user_can_buy_one_item(
    logged_in,
    cart_page,
    checkout_info_page,
    checkout_overview_page,
    checkout_complete_page,
):
    # Happy path: catalog -> cart -> info -> overview -> thank you.
    logged_in.add_to_cart(BACKPACK)
    logged_in.open_cart()

    expect(cart_page.page_title).to_have_text("Your Cart")
    assert BACKPACK in cart_page.item_names_in_cart()

    cart_page.checkout()
    customer = get_customer()
    checkout_info_page.fill_info(
        customer["first_name"],
        customer["last_name"],
        customer["postal_code"],
    )

    expect(checkout_overview_page.page_title).to_have_text("Checkout: Overview")
    expect(checkout_overview_page.total).to_contain_text("$32.39")

    checkout_overview_page.finish()

    expect(checkout_complete_page.header).to_have_text("Thank you for your order!")
