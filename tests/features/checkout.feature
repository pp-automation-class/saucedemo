Feature: Checkout
  Happy path: catalog -> cart -> info -> overview -> thank you.

  Background:
    Given a standard user is logged in

  Scenario: User can buy one item
    When the user adds "Sauce Labs Backpack" to the cart
    And the user opens the cart
    Then the cart title is "Your Cart"
    And the cart contains "Sauce Labs Backpack"
    When the user starts checkout
    And the user enters a new customer
    Then the overview title is "Checkout: Overview"
    And the order total contains "$32.39"
    When the user finishes the order
    Then the order confirmation is "Thank you for your order!"
