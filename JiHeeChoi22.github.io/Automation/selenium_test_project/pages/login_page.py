from .base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Login']")
    ERROR_MESSAGE = (By.CLASS_NAME, "alert-danger")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://demo.opencart.com/index.php?route=account/login"

    def open(self):
        self.driver.get(self.url)

    def login(self, username, password):
        self.input_text(self.USERNAME_INPUT, username)
        self.input_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def is_login_successful(self):
        return "account" in self.driver.current_url 