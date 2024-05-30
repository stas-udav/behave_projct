from behave import step
from selenium import webdriver
import time

from selenium.webdriver.common.by import By


@step('Verify if open web-site is eBay.com')
def test_verify_main_page_link(context):
    current_url = context.driver.current_url
    assert current_url == 'https://www.ebay.com/', f"Expected url 'eBay.com' but opened url '{current_url}'"
    time.sleep(1)


@step('verify corresponding page after click on "{box}" button')
def daily_deals_url_check(context, box):
    daily_deals_button = context.driver.find_element(By.XPATH, f'//*[contains(@class, "gh-") and text() = "{box}"]')
    daily_deals_button.click()

    # getting current URL after click and validate if url correct
    current_url = context.driver.current_url
    expected_url = expected_urls.get(box)
    assert current_url == expected_url, f"Expected url '{expected_url}' but opened url '{current_url}' "
    time.sleep(2)


expected_urls = {
    " Daily Deals": "https://www.ebay.com/deals",
    " Brand Outlet": "https://www.ebay.com/b/Brand-Outlet/bn_7115532402",
    " Gift Cards": "https://www.ebay.com/giftcards",
    " Help & Contact": "https://www.ebay.com/help/home",
}
