from behave import step
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@step('check if carousel is present on page')
def carousel_menu_check(context):
    time.sleep(10)
    menu_list = []
    menu_title = []
    issue = []
    carousel_menus = (WebDriverWait(context.driver, 15).
                      until(EC.presence_of_all_elements_located((By.XPATH,
                                                                 '//div[@class="carousel__viewport"]/ul[@class="carousel__list"]/li[@class="carousel__snap-point vl-carousel__item"][div[@data-view]]'))))

    context.carousel_elements = carousel_menus
    # print(len(carousel_menus))

    # checking if all 4 slides is present
    for menu in carousel_menus:
        menu_list.append(menu)
        menu_title.append(menu.text)
        # print(menu.get_attribute('aria-hidden'))
    # print(len(menu_list))
    if len(menu_list) != 4:
        issue.append(f"Carousel images < then required, {len(menu_list)}")

    if issue:
        raise Exception(f'issue was discovered: \n{issue}')

@step('check if carousel is rolling and all "{img}" slides is present')
def carousel_rolling_check(context, img):
    issue = []
    visible_image = 0
    carousel_menus = context.carousel_elements
    img = int(img)

    # checking visibility of each menu
    for menu in carousel_menus:
        try:
            WebDriverWait(context.driver, 15).until(EC.visibility_of(menu))
        except TimeoutException:
            issue.append(f"Element {menu.text} not visible")
        if menu.is_displayed():
            visible_image += 1
            # print(visible_image)
    if visible_image != img:
        issue.append(f"Carousel images showed < then required images, showed :{visible_image}")

    if issue:
        raise Exception(f'issue was discovered: \n{issue}')
    # print((img))
    # print(visible_image)

@step('buttons play, pause, left, right is present')
def carousel_buttons(context):
    issue = []

    buttons = {
        'previous_button': "//button[@aria-label = 'Go to previous banner']",
        'next_button': "//button[@aria-label = 'Go to next banner']",
        'pause_button': '//button[@aria-label="Pause Banner Carousel"]',
        'play_button': '//button[@aria-label="Play Banner Carousel"]',
    }
    context.carousel_buttons = {}
    carousel_menus = context.carousel_elements

    for button, xpath in buttons.items():
        attribute_menu_before = []
        attribute_menu_after = []

        for menu in carousel_menus:

            # get status carousel menu (visible\invisible) before click
            attribute_menu_before.append(menu.get_attribute('aria-hidden'))
            # print(attribute_menu_before)

        try:
            button_element = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            button_element.click()
            WebDriverWait(context.driver, 10).until(
                lambda driver: all(menu.get_attribute('aria-hidden') != attribute_menu_before[i] for i, menu in
                                   enumerate(carousel_menus)))
        except TimeoutException:
            issue.append(f"{button} not visible")

    if issue:
        raise Exception(f'issue was discovered: \n{issue}')
    #         time.sleep(1)
    #         if menu.get_attribute('aria-hidden') == attribute_menu_before[carousel_menus.index(menu)]:
    #             issue.append(f"Element {button} not work {menu.text}")
    #         # get status carousel menu (visible/invisible) after click
    #         # for menu in carousel_menus:
    #         #     attribute_menu_after.append(menu.get_attribute('aria-hidden'))
    #         #     # print(attribute_menu_after)
    #         #     if menu.get_attribute('aria-hidden') == attribute_menu_before[carousel_menus.index(menu)]:
    #         #         issue.append(f"Element {button} not work")
    #         attribute_menu_before.clear()
    #         attribute_menu_after.clear()
    #     except TimeoutException:
    #         issue.append(f"{button} not visible")
    #
    # if issued:
    #     raise Exception(issue was discovered: \n{issue}')

