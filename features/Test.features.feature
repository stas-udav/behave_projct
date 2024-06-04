# Created by stanh at 03.05.2024
Feature: eBay regression

  # 
  Background: Generic navigation 
    Given Navigate to eBay.com

  Scenario:User should be able to add item to the cart

    
    When enter "dress" to the searchbar
    And click the "Search" button
#    Then click to the 1st dress from the page
#    And click add to cart

  Scenario: Filter validation - length
    When enter "dress" to the searchbar
    And click the "Search" button
    Then Filter "Dress Length" by "Midi"
    And Size filter "Regular Size" by "S"
    Then Choose dress "Blue"

  Scenario: Search validation
    When enter "dress" to the searchbar
    And click the "Search" button
    Then all items are "dress" related from "6" to "3" pages

  Scenario Outline: Validation item search
    When enter "<item>" to the searchbar
    And click the "Search" button
    Then all items are "<item>" related from "<starting_page>" to "<desired_page>" pages
    Examples:
      |item | starting_page| desired_page|
      |Dress | 5           | 8           |
      |Iphone| 8           |3            |



#  Scenario: Flying menu validation
#    And click on the "Shop by category" menu
  Scenario: Flying menu validation
    And click on the "Shop by category" menu
    Then check following menus contains submenus
      | Motors                 | Electronics                              |Collectibles & Art|
      | Parts& accessories    | Computers, Tablets & Network Hardware    |Trading Cards|
      | Cars & trucks          | Cell Phones, Smart Watches & Accessories |Collectibles|
      | Motorcycles            | Video Games & Consoles                   |Coins & Paper Money           |
      | Other vehicles         | Cameras & Photo                          |Sports Memorabilia                   |


  Scenario: Carousel menu validation
    And check if carousel is present on page


   Scenario: Filter validation for item specs
    When enter "dress" to the searchbar
    And click the "Search" button
    Then Filter "Dress Length" by "Midi"
    Then Validate "Dress Length" are "Midi"