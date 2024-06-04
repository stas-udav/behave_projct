from behave import step
from selenium import webdriver
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

    carousel_menus = (WebDriverWait(context.driver, 10).
                      until(EC.presence_of_all_elements_located((By.XPATH,
                                                                 '//div[@class="carousel__viewport"]/ul[@class="carousel__list"]/li[@class="carousel__snap-point vl-carousel__item" and (@aria-hidden="true")]/div[@data-view]'))))
    # print(len(carousel_menus))
    for menu in carousel_menus:
        menu_list.append(menu)
        menu_title = menu.text
        print(menu_title)
    # initial_items = [item.get_attribute('aria-hidden="true"') for item in menu_list]
    # print(menu_list)
    # print(initial_items)
