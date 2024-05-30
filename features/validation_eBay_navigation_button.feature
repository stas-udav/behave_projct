Feature: validation of eBay.com header navigation


  Scenario: Users should be able to click on navigation buttons
  in the header bar and be redirected to the corresponding pages

    Given  Navigate to eBay.com
    And Verify if open web-site is eBay.com
    When verify corresponding page after click on " Daily Deals" button
    And verify corresponding page after click on " Brand Outlet" button
    Then verify corresponding page after click on " Gift Cards" button
    And verify corresponding page after click on " Help & Contact" button
