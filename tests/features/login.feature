Feature: Login

  @Smoke
  Scenario: Standard user reaches the inventory
    Given the login page is open
    When the user logs in as "standard"
    Then the inventory title is "Products"
    And the page url is "/inventory.html"

  @Smoke
  Scenario: Locked out user sees an error
    Given the login page is open
    When the user logs in as "locked_out"
    Then the login error contains "locked out"
    And the page url is "/"

  Scenario: Invalid username
    Given the login page is open
    When the user logs in as "invalid"
    Then the login error contains "invalid"
    And the page url is not "/"

  Scenario: Invalid password
    Given the login page is open
    When the user logs in as "invalid_password"
    Then the login error contains "invalid"
    And the page url is "/"

  Scenario: Empty username
    Given the login page is open
    When the user logs in as "empty"
    Then the login error contains "invalid"
    And the page url is "/"

