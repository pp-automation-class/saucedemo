Feature: Inventory  

  Background:
    Given a standard user is logged in

  Scenario: Catalog lists products
    Then the catalog contains "Sauce Labs Backpack"
    And the catalog has 6 products

  Scenario: Add to cart updates the badge
    Then the cart has 0 items
    When the user adds "Sauce Labs Backpack" to the cart
    Then the cart badge shows "1"
