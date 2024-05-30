from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import os
import re


def before_all(context):
    ...


def before_feature(context, feature):
    context.url = "https://www.ebay.com"


def before_scenario(context, scenario):
    print(f"before_scenario is called for scenario: {scenario.name}")
    context.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    # context.driver = webdriver.Chrome()
    context.driver.maximize_window()


def after_step(context, step):
    if step.status == "failed":
        # print(step.name)
        current = os.path.dirname(__file__)
        # print(current)
        screenshots_path = os.path.abspath(os.path.join(current, "screenshots"))
        # print(screenshots_path)
        sanitized_screenshot_name = re.sub(r'[<>:"/\\|?*]', '_', step.name)
        context.driver.save_screenshot(os.path.join(screenshots_path, f"{sanitized_screenshot_name}.png"))
        # context.driver.save_screenshot("screenshot.png")



def after_scenario(context, scenario):
    context.driver.close()
    context.driver.quit()
