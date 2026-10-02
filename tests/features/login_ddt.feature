@login @ddt
Feature: Login (data-driven)

  Each Scenario Outline runs once per row of its Examples table.

  Scenario Outline: Valid user "<role>" reaches the inventory
    Given the login page is open
    When the user logs in as "<role>"
    Then the inventory title is "Products"
    And the page url is "/inventory.html"

    Examples:
      | role               |
      | standard           |
      | problem            |
      | performance_glitch |
      | error              |
      | visual             |

  Scenario Outline: Locked out user "<role>" sees an error
    Given the login page is open
    When the user logs in as "<role>"
    Then the login error contains "<error>"
    And the page url is "/"

    Examples:
      | role       | error                                 |
      | locked_out | Sorry, this user has been locked out. |

  Scenario Outline: Invalid credentials show an error
    Given the login page is open
    When the user logs in with username "<username>" and password "<password>"
    Then the login error contains "<error>"
    And the page url is "/"

    Examples:
      | username      | password     | error                                                       |
      | invalid_user  | secret_sauce | Username and password do not match any user in this service |
      | standard_user | wrong_pass   | Username and password do not match any user in this service |
      |               | secret_sauce | Username is required                                        |
      | standard_user |              | Password is required                                        |
      |               |              | Username is required                                        |
