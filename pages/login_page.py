import logging

from playwright.sync_api import Page

from pages.base_page import BasePage

log = logging.getLogger(__name__)


class LoginPage(BasePage):
    """https://www.saucedemo.com/ — the only public screen."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username = page.locator("[data-test='username']")
        self.password = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")
        self.error = page.locator("[data-test='error']")

    def open(self, path: str = "/") -> None:
        super().open(path)

    def login(self, username: str, password: str) -> None:
        """One method = one user action. Tests should not fill fields themselves."""
        # Never log the password.
        log.info("Log in as %s", username)
        self.fill(self.username, username)
        self.fill(self.password, password)
        self.click(self.login_button)
