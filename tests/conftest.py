"""Steps shared by more than one feature."""

from tests.cucumber import given, when


@given("a standard user is logged in")
def standard_user_is_logged_in(logged_in):
    return logged_in


@when("the user adds {string} to the cart")
def user_adds_product(logged_in, string):
    logged_in.add_to_cart(string)
