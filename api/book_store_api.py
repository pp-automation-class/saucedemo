"""DemoQA Book Store API — https://demoqa.com/swagger

One method = one endpoint. Tests never build URLs or headers themselves.
Most endpoints need `Authorization: Bearer <token>`; call `login()` first.
"""

import logging

import allure
import requests

log = logging.getLogger(__name__)

BASE_URL = "https://demoqa.com"


class BookStoreApi:
    def __init__(self, base_url: str = BASE_URL, timeout: float = 30) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        # Filled by login(). Shared with the browser so UI and API use one session.
        self.token: str | None = None
        self.token_expires: str | None = None

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        # Never log request bodies: they hold the password.
        response = self.session.request(
            method, self.base_url + path, timeout=self.timeout, **kwargs
        )
        log.info("%s %s -> %s", method, path, response.status_code)
        allure.attach(
            response.text or "<empty>",
            name=f"{method} {path} -> {response.status_code}",
            attachment_type=allure.attachment_type.TEXT,
        )
        return response

    # ---------- Account ----------

    @allure.step("Create user {username}")
    def create_user(self, username: str, password: str) -> requests.Response:
        return self._request(
            "POST",
            "/Account/v1/User",
            json={"userName": username, "password": password},
        )

    @allure.step("Generate token for {username}")
    def generate_token(self, username: str, password: str) -> requests.Response:
        return self._request(
            "POST",
            "/Account/v1/GenerateToken",
            json={"userName": username, "password": password},
        )

    def login(self, username: str, password: str) -> None:
        """Get a token and send it with every next request.

        DemoQA keeps only the newest token per user: generating another one
        (API or UI login form) makes this one invalid.
        """
        body = self.generate_token(username, password).json()
        self.token, self.token_expires = body["token"], body["expires"]
        self.session.headers["Authorization"] = f"Bearer {self.token}"

    @allure.step("Get user {user_id}")
    def get_user(self, user_id: str) -> requests.Response:
        return self._request("GET", f"/Account/v1/User/{user_id}")

    @allure.step("Delete user {user_id}")
    def delete_user(self, user_id: str) -> requests.Response:
        return self._request("DELETE", f"/Account/v1/User/{user_id}")

    # ---------- BookStore ----------

    @allure.step("Get all books")
    def get_books(self) -> requests.Response:
        return self._request("GET", "/BookStore/v1/Books")

    @allure.step("Add book {isbn} to user {user_id}")
    def add_book(self, user_id: str, isbn: str) -> requests.Response:
        return self._request(
            "POST",
            "/BookStore/v1/Books",
            json={"userId": user_id, "collectionOfIsbns": [{"isbn": isbn}]},
        )

    @allure.step("Delete all books of user {user_id}")
    def delete_all_books(self, user_id: str) -> requests.Response:
        return self._request(
            "DELETE", "/BookStore/v1/Books", params={"UserId": user_id}
        )

    @allure.step("Delete book {isbn} from user {user_id}")
    def delete_book(self, user_id: str, isbn: str) -> requests.Response:
        return self._request(
            "DELETE",
            "/BookStore/v1/Book",
            json={"isbn": isbn, "userId": user_id},
        )
