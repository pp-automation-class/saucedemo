"""DemoQA Book Store — API and UI in one test.

API:  create user          UI:  add 3 books
API:  delete 1 book        UI:  2 books left
API:  delete books + user  UI:  login says the user does not exist

Setup and cleanup go through the API (fast, reliable); the UI is used
only for what we actually want to check in the browser.
"""

import allure
from playwright.sync_api import expect

from pages.book_store_pages import BookPage, BookStoreLoginPage, ProfilePage


@allure.feature("Book Store API + UI")
@allure.title("API user, UI adds 3 books, API deletes 1, UI shows 2, user gone")
def test_books_added_in_ui_and_removed_by_api(page, book_api, book_store_ui):
    user = book_store_ui
    profile = ProfilePage(page)

    with allure.step("API: pick 3 books from the store"):
        response = book_api.get_books()
        assert response.status_code == 200, response.text
        books = response.json()["books"][:3]
        assert len(books) == 3, "store has fewer than 3 books"
        titles = [b["title"] for b in books]

    with allure.step("UI: user is logged in (token shared from API)"):
        profile.open()
        expect(profile.user_name).to_have_text(user["username"])
        expect(profile.book_links).to_have_count(0)

    with allure.step("UI: add 3 books to the collection"):
        book_page = BookPage(page)
        for book in books:
            book_page.open(book["isbn"])
            assert book_page.add_to_collection() == "Book added to your collection."

        profile.open()
        expect(profile.book_links).to_have_text(titles)

    with allure.step("API: the 3 books are saved on the server"):
        saved = book_api.get_user(user["id"]).json()["books"]
        assert [b["isbn"] for b in saved] == [b["isbn"] for b in books]

    removed, kept = books[0], books[1:]
    with allure.step(f"API: delete '{removed['title']}'"):
        response = book_api.delete_book(user["id"], removed["isbn"])
        assert response.status_code == 204, response.text

    with allure.step("UI: 2 books are left"):
        profile.open()
        expect(profile.book_links).to_have_count(2)
        expect(profile.book_links).to_have_text([b["title"] for b in kept])

    with allure.step("API: delete all books, then the user"):
        response = book_api.delete_all_books(user["id"])
        assert response.status_code == 204, response.text
        assert book_api.get_user(user["id"]).json()["books"] == []

        response = book_api.delete_user(user["id"])
        assert response.status_code == 204, response.text

    with allure.step("UI: the user can no longer log in"):
        page.context.clear_cookies()
        login = BookStoreLoginPage(page)
        login.open()
        login.login(user["username"], user["password"])
        expect(login.error).to_have_text("Invalid username or password!")
        expect(page).to_have_url("https://demoqa.com/login")
