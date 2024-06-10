from behave import step
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re


@step('Select a filter')
def filter_select(context):
    issue = []

    # Iterate through context.table to extract "title_name" and "title_value" for each row
    for row in context.table:
        filter_title_user_data = row[0]
        filter_value_user_data = row[1]
        # print(filter_value_user_data)
        if filter_title_user_data == 'Dress Length':
            xpath = f'//input[@aria-label="{filter_value_user_data}"]'

        elif filter_title_user_data == 'Color':
            xpath = f'//span[text()="{filter_value_user_data}"]'
        filter_title = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                               f'//div[text() = "{filter_title_user_data}"]')))

        # print(xpath)
        filter_value = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                               xpath)))
        try:
            context.driver.execute_script("arguments[0].click();", filter_value)

        except:
            issue.append(f"Checkbox '{filter_value_user_data}' does not exist'")
        # print(filter_value.get_attribute('aria-label'), filter_title.text)


@step('Validate filters')
def dress_length_validation(context):
    issue = []

    for row in context.table:
        filter_title_user_data = row['Filter']
        filter_value_user_data = row['Value']

        if filter_title_user_data == 'Dress Length':
            xpath = f'//input[@aria-label="{filter_value_user_data}"]'
        elif filter_title_user_data == 'Color':
            xpath = f'//span[text()="{filter_value_user_data}"]'
        else:
            raise ValueError(f"Unsupported filter title: {filter_title_user_data}")

        # Click the filter
        filter_value = wait_for_element(context.driver, xpath)
        context.driver.execute_script("arguments[0].click();", filter_value)

        # Allow time for page to refresh with new filter applied
        time.sleep(2)

        # Validate the filter
        all_items = WebDriverWait(context.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@id, "item")]')))
        main_tab = context.driver.current_window_handle

        for item in all_items:
            title = item.find_element(By.XPATH, './/span[@role = "heading"]').text
            item_url = item.find_element(By.XPATH, './/a[@class = "s-item__link"]').get_attribute('href')
            context.driver.execute_script(f"window.open('{item_url}')")
            context.driver.switch_to.window(context.driver.window_handles[-1])

            all_labels = WebDriverWait(context.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//dt[@class="ux-labels-values__labels"]')))
            all_values = WebDriverWait(context.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//dd[@class="ux-labels-values__values"]')))

            all_labels_text = [label.text for label in all_labels]
            all_values_text = [value.text for value in all_values]

            item_specs = dict(zip(all_labels_text, all_values_text))

            if filter_title_user_data in item_specs and filter_value_user_data not in item_specs[
                filter_title_user_data]:
                issue.append(
                    f"'{title}' is not related to '{filter_value_user_data}' by '{filter_title_user_data}'")

            context.driver.close()
            context.driver.switch_to.window(main_tab)

        if issue:
            raise AssertionError(f"Issues found: {issue}")
def wait_for_element(driver, xpath):
        return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))


    # all_items = (WebDriverWait(context.driver, 2).
    #              until(EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@id, "item")]'))))
    # # print(len(all_items))
    #
    # # current page
    # main_tab = context.driver.current_window_handle
    # issue = []
    #
    # for item in all_items:
    #     title = item.find_element(By.XPATH, './/span[@role = "heading"]').text
    #     item_url = item.find_element(By.XPATH, './/a[@class = "s-item__link"]').get_attribute('href')
    #
    #     # switch to the item page
    #     context.driver.execute_script(f"window.open('{item_url}')")
    #     context.driver.switch_to.window(context.driver.window_handles[-1])  # switch to the new opened tab
    #
    #     # collect item spec
    #     all_labels = (WebDriverWait(context.driver, 2).
    #                   until(EC.presence_of_all_elements_located((By.XPATH, '//dt[@class="ux-labels-values__labels"]'))))
    #     all_values = (WebDriverWait(context.driver, 2).
    #                   until(EC.presence_of_all_elements_located((By.XPATH, '//dd[@class="ux-labels-values__values"]'))))
    #
    #     # get text from items
    #     all_labels_text = []
    #     for label in all_labels:
    #         all_labels_text.append(label.text)
    #
    #     # get text from values
    #     all_values_text = []
    #     for values in all_values:
    #         all_values_text.append(values.text)
    #
    #     item_specs = dict(zip(all_labels_text, all_values_text))
    #
    #     # if [re.search(rf'\b{expected_value}\b', item_specs[key_name] )] in item_specs[key_name]:
    #     if expected_value in item_specs[key_name]:
    #         print(key_name, item_specs[key_name], item_specs[key_name])
    #         issue.append(f"'{title}' is not related to '{expected_value}' by '{key_name}'")
    #
    #     if issue:
    #         print(issue)
    #     # print(all_labels_text, all_values_text)
    #     # Close the new tab and switch back to the main tab
    #     context.driver.close()
    #     context.driver.switch_to.window(main_tab)
