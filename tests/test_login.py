import allure
from playwright.sync_api import expect
from pytest_bdd import scenario

from data.users import get_user
from tests.cucumber import given, then, when


@allure.feature("Login")
@scenario("features/login.feature", "Standard user reaches the inventory")
def test_standard_user_reaches_inventory():
    pass


@allure.feature("Login")
@scenario("features/login.feature", "Locked out user sees an error")
def test_locked_out_user_sees_error():
    pass


@given("the login page is open")
def login_page_is_open(login_page):
    login_page.open()


@when("the user logs in as {string}")
def user_logs_in_as(login_page, string):
    login_page.login(*get_user(string))


@then("the inventory title is {string}")
def inventory_title_is(inventory_page, string):
    expect(inventory_page.page_title).to_have_text(string)


@then("the page url is {string}")
def page_url_is(login_page, string):
    expect(login_page.page).to_have_url(string)


@then("the login error contains {string}")
def login_error_contains(login_page, string):
    expect(login_page.error).to_be_visible()
    expect(login_page.error).to_contain_text(string)


@then("the page url is not {string}")
def page_url_is_not(login_page, string):
    expect(login_page.page).not_to_have_url(string)
