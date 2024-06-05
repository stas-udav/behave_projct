from behave import step
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# //div[@class="carousel__viewport"]/ul/li[@class="carousel__snap-point vl-carousel__item"]
#
# //div[@class="carousel__viewport"]
#
# //div[@class="carousel__viewport"]/ul[@class="carousel__list"]/li
#
# //div[@class="carousel__viewport"]/ul[@class="carousel__list"]/li[@class="carousel__snap-point vl-carousel__item"]/div[@data-view]
#
# //div[@class="carousel__viewport"]/ul[@class="carousel__list"]/li[@class="carousel__snap-point vl-carousel__item" and not(@aria-hidden="true")]/div[@data-view]

@step('check if carousel is present on page')
def step_impl(context):
    time.sleep(10)
    menu_list = []
    menu_title = []
    issue = []
    visible_image = 0
    carousel_menus = (WebDriverWait(context.driver, 10).
                      until(EC.presence_of_all_elements_located((By.XPATH,
                                                                 '//div[@class="carousel__viewport"]/ul[@class="carousel__list"]/li[@class="carousel__snap-point vl-carousel__item"]/div[@data-view]'))))

    # print(len(carousel_menus))

    # checking if all 4 slides is present
    for menu in carousel_menus:
        menu_list.append(menu)
        menu_title.append(menu.text)
    # print(len(menu_list))
    if len(menu_list) != 4:
        issue.append(f"Carousel images < then required, {len(menu_list)}")
    # initial_items = [item.get_attribute('aria-hidden="true"') for item in menu_list]
    # print(menu_list)
    # print(initial_items)
    # checking visibility of each menu
    for menu in carousel_menus:
        try:
            WebDriverWait(context.driver, 10).until(EC.visibility_of(menu))
        except TimeoutException:
            issue.append(f"Element {menu.text} not visible")
        if menu.is_displayed():
            visible_image += 1

    if issue:
        raise Exception (f'issue was discovered: \n{issue}')
    print(visible_image)
#//div[@class="carousel__viewport"]/ul[@class="carousel__list"]//following-sibling::li[@class="carousel__snap-point vl-carousel__item"]