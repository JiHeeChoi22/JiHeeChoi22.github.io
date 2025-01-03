from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from utilities.test_helper import TestHelper

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.helper = TestHelper()

    def find_element(self, locator):
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def click_element(self, locator):
        self.wait.until(
            EC.element_to_be_clickable(locator)
        ).click()

    def input_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find_element(locator).text

    def is_element_visible(self, locator):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
        except:
            return False 

    def find_elements(self, locator):
        return self.wait.until(
            EC.presence_of_all_elements_located(locator)
        )

    def select_by_visible_text(self, locator, text):
        element = self.find_element(locator)
        Select(element).select_by_visible_text(text) 