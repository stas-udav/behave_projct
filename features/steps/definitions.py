from behave import step
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time


@step('Navigate to eBay.com')
def test(context):
    # context.driver = webdriver.Chrome()
    # context.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    # context.driver.maximize_window()
    context.driver.get(context.url)


@step('enter "dress" to the searchbar')
def enter_credentials_searchbar(context):
    searchbar = context.driver.find_element(By.XPATH, '//input[@aria-label="Search for anything"]')
    searchbar.send_keys('dress')


@step('click the "Search" button')
def click_search_button(context):
    search_button = context.driver.find_element(By.XPATH, '//input[@type="submit"]')
    search_button.click()


@step('click to the 1st dress from the page')
def click_on_the_1st_item(context):
    first_item = context.driver.find_element(By.XPATH,
                                             '//div[@class="s-item__title"]')
    time.sleep(2)
    first_item.click()
    time.sleep(1)


@step('click add to cart')
def add_to_cart(context):
    add_to_cart.button = context.driver.find_element(By.XPATH, '//a[@id="atcBtn_btn_1"]')
    add_to_cart.button.click()
    time.sleep(0.5)


@step('Filter "{filter_name}" by "{check_box_name}"')
def check_box(context, filter_name, check_box_name):
    check_box_filter = context.driver.find_element(By.XPATH,
                                                   f'//li[@class="x-refine__main__list "][//div[text() = "{filter_name}"]]//div[@class="x-refine__select__svg"][.//span[text() = "{check_box_name}"]]//input')
    check_box_filter.click()
    time.sleep(1)


@step('Size filter "{size_filter}" by "{size_value}"')
def check_box(context, size_filter, size_value):
    check_box_filter = context.driver.find_element(By.XPATH,
                                                   f"//li[@class='x-refine__main__list '][.//div[text()='Size']]//div[@class='size-component__container']//span[text()='{size_filter}']/following-sibling::span[text()='{size_value}']")
    check_box_filter.click()
    time.sleep(1)


@step('Choose dress "{color}"')
def check_box(context, color):
    check_box_filter = context.driver.find_element(By.XPATH,
                                                   f"//li[@class='x-refine__main__list '][.//div[text()='Color']]//a[@style='background-color: #657EEA']/span[text()='{color}']")
    context.driver.execute_script("arguments[0].click();", check_box_filter)
    time.sleep(1)


@step('all items are "{desired_title}" related from "{current_page}" to "{maximum_pages}" pages')
def all_item_title(context, desired_title, current_page, maximum_pages):
    issue = []
    maximum_pages = int(maximum_pages)
    current_page_number = int(current_page)

    # Go to the starting page
    starting_page = context.driver.find_element(By.XPATH, f'//li/a[@class="pagination__item"][text()="{current_page}"]')
    starting_page.click()
    time.sleep(2)

    def check_item_on_page():
        all_items = context.driver.find_elements(By.XPATH, '//li[contains(@id, "item")]//span[@role="heading"]')
        for item in all_items:
            title = item.text
            if desired_title.lower() not in title.lower():
                issue.append(f'{title} is not {desired_title} related')

    if current_page_number < maximum_pages:
        while current_page_number <= maximum_pages:
            # Find all items on the current page
            check_item_on_page()
            # increase number of  the current page
            current_page_number += 1

            # Check if there are more pages to navigate
            if current_page_number <= maximum_pages:
                next_page_button = context.driver.find_element(By.XPATH, '//a[@aria-label="Go to next search page"]')
                next_page_button.click()
                time.sleep(2)  # Wait for the next page to load

    else:
        while current_page_number > maximum_pages:
            # Find all items on the current page
            check_item_on_page()
            current_page_number -= 1

            if current_page_number >= maximum_pages:
                previous_page_button = context.driver.find_element(By.XPATH,
                                                                   '//a[@aria-label="Go to previous search page"]')
                previous_page_button.click()
                time.sleep(2)

    if issue:
        raise Exception(f' Issues discovered:\n{issue}')


@step('enter "{item}" to the searchbar')
def step_impl(context, item):
    searchbar = context.driver.find_element(By.XPATH, '//input[@aria-label="Search for anything"]')
    searchbar.send_keys(item)


@step('click on the "Shop by category" menu')
def step_impl(context):
    shop_by_category = context.driver.find_element(By.XPATH, '//button[@id="gh-shop-a"]')
    shop_by_category.click()
    time.sleep(10)


@step('check following menus contains submenus')
def step_impl(context):

    exclusions = ["All Brands", "All Categories", "Seasonal Sales & Events"]
    menus = context.driver.find_elements(By.XPATH, '//td//h3[@class="gh-sbc-parent"]/a')
    menu_title = {}
    issue = []
    for menu in menus:
        menu_t = menu.text
        # print(menu_title)
        if menu_t not in exclusions:
            menu_title[menu_t] = []
    time.sleep(0.5)

    for menu in menu_title.keys():
        if menu not in exclusions:
            # print(menu)
            submenus = context.driver.find_elements(By.XPATH,
                                                    f'//td//h3/a[text()="{menu}"]/parent::h3/following-sibling::ul[1]/li/a')
            for submenu in submenus:
                submenu_t = submenu.text
                menu_title[menu].append(submenu_t)
                # print(submenu_t)
    # print(menu_title)
    def compare_menu_vs_userdata():
        headings = context.table.headings
        table_dict = {}
        for heading in headings:
            table_dict[heading] = []
        # print(headings)
        for row in context.table.rows:
            for heading in row.headings:
                table_dict[heading].append(row[heading])
            # print(table_dict)
        if menu_title != table_dict:
            issue.append(f'\n{menu_title}, {table_dict}')
            raise Exception(f'Menu titles {menu_title} do not match {table_dict}')

    compare_menu_vs_userdata()