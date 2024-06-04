from behave import step
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@step('Validate "{key_name}" are "{expected_value}"')
def dress_length_validation(context, key_name, expected_value):
    all_items = (WebDriverWait(context.driver, 2).
                 until(EC.presence_of_all_elements_located((By.XPATH,'//li[contains(@id, "item")]'))))
    # print(len(all_items))

    # current page
    main_tab = context.driver.current_window_handle
    issue = []

    for item in  all_items:
        title = item.find_element(By.XPATH, './/span[@role = "heading"]').text
        item_url = item.find_element(By.XPATH, './/a[@class = "s-item__link"]').get_attribute('href')

        # switch to the item page
        context.driver.execute_script(f"window.open('{item_url}')")
        context.driver.switch_to.window(context.driver.window_handles[-1])  # switch to the new opened tab

        # collect item spec
        all_labels = (WebDriverWait(context.driver, 2).
                      until(EC.presence_of_all_elements_located((By.XPATH, '//dt[@class="ux-labels-values__labels"]'))))
        all_values = (WebDriverWait(context.driver, 2).
                      until(EC.presence_of_all_elements_located((By.XPATH, '//dd[@class="ux-labels-values__values"]'))))

        # get text from items
        all_labels_text = []
        for label in all_labels:
            all_labels_text.append(label.text)


        # get text from values
        all_values_text = []
        for values in all_values:
            all_values_text.append(values.text)

        item_specs = dict(zip(all_labels_text, all_values_text))

        if item_specs[key_name] != [expected_value]:
            issue.append(f"'{title}' is not related to '{expected_value}' by '{key_name}'")

        if issue:
            print(issue)
        # print(all_labels_text, all_values_text)
        # Close the new tab and switch back to the main tab
        context.driver.close()
        context.driver.switch_to.window(main_tab)
