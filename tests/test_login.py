import allure
from playwright.sync_api import expect

from data.users import get_user


@allure.feature("Login")
def test_standard_user_reaches_inventory(login_page, inventory_page):
    login_page.open()
    login_page.login(*get_user("standard"))

    expect(inventory_page.page_title).to_have_text("Products")
    expect(inventory_page.page).to_have_url("/inventory.html")


@allure.feature("Login")
def test_locked_out_user_sees_error(login_page):
    login_page.open()
    login_page.login(*get_user("locked_out"))

    expect(login_page.error).to_be_visible()
    expect(login_page.error).to_contain_text("locked out")
    expect(login_page.page).to_have_url("/")
