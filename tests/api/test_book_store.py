"""DemoQA Book Store: user -> add book -> delete book -> delete user.

Swagger: https://demoqa.com/swagger
"""

import allure


@allure.feature("Book Store API")
@allure.title("Create user, add one book, delete the book, delete the user")
def test_user_book_lifecycle(book_api, book_user):
    user_id = book_user["id"]

    with allure.step("Pick the first book from the store"):
        response = book_api.get_books()
        assert response.status_code == 200, response.text
        book = response.json()["books"][0]
        isbn = book["isbn"]

    with allure.step("Add the book to the user"):
        response = book_api.add_book(user_id, isbn)
        assert response.status_code == 201, response.text
        assert response.json() == {"books": [{"isbn": isbn}]}

        books = book_api.get_user(user_id).json()["books"]
        assert [b["isbn"] for b in books] == [isbn]
        assert books[0]["title"] == book["title"]

    with allure.step("Delete the book from the user"):
        response = book_api.delete_book(user_id, isbn)
        assert response.status_code == 204, response.text

        assert book_api.get_user(user_id).json()["books"] == []

    with allure.step("Delete the user"):
        response = book_api.delete_user(user_id)
        assert response.status_code == 204, response.text

        response = book_api.get_user(user_id)
        assert response.status_code == 401
        assert response.json()["message"] == "User not found!"
