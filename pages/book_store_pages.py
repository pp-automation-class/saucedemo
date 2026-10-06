"""DemoQA Book Store screens — https://demoqa.com/books

Not Sauce Demo, so every URL is absolute (pytest --base-url points at Sauce).
"""

import logging

from playwright.sync_api import Page

from pages.base_page import BasePage

log = logging.getLogger(__name__)

DEMOQA = "https://demoqa.com"


class BookStoreLoginPage(BasePage):
    """https://demoqa.com/login"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username = page.locator("#userName")
        self.password = page.locator("#password")
        self.login_button = page.locator("#login")
        # Red text under the form: "Invalid username or password!"
        self.error = page.locator("#name")

    def open(self, path: str = "/login") -> None:
        super().open(DEMOQA + path)

    def login(self, username: str, password: str) -> None:
        log.info("Book Store log in as %s", username)
        self.fill(self.username, username)
        self.fill(self.password, password)
        self.click(self.login_button)


class BookPage(BasePage):
    """https://demoqa.com/books?search=<isbn> — one book's details."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.add_button = page.get_by_role("button", name="Add To Your Collection")

    def open(self, isbn: str) -> None:
        super().open(f"{DEMOQA}/books?search={isbn}")

    def add_to_collection(self) -> str:
        """Click Add and return the alert text the site shows.

        "Book added to your collection." on success,
        "Book already present in the your collection!" for a duplicate.
        """
        with self.page.expect_event("dialog") as dialog_info:
            self.click(self.add_button)
        dialog = dialog_info.value
        message = dialog.message
        dialog.accept()
        log.info("Add to collection -> %s", message)
        return message


class ProfilePage(BasePage):
    """https://demoqa.com/profile — the user's book collection."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.user_name = page.locator("#userName-value")
        # Each title in the collection table links to /books?search=<isbn>.
        self.book_links = page.locator("table tbody a[href*='/books?search=']")

    def open(self, path: str = "/profile") -> None:
        super().open(DEMOQA + path)

    def book_titles(self) -> list[str]:
        return self.book_links.all_inner_texts()
