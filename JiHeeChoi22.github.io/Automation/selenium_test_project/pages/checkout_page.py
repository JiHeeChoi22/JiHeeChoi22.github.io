from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutPage(BasePage):
    # Locators - 체크아웃 단계별 요소들
    GUEST_CHECKOUT_RADIO = (By.CSS_SELECTOR, "input[value='guest']")
    CONTINUE_BUTTON = (By.ID, "button-account")
    
    # 개인정보 입력 폼 필드
    FIRST_NAME = (By.ID, "input-payment-firstname")
    LAST_NAME = (By.ID, "input-payment-lastname")
    EMAIL = (By.ID, "input-payment-email")
    TELEPHONE = (By.ID, "input-payment-telephone")
    ADDRESS_1 = (By.ID, "input-payment-address-1")
    CITY = (By.ID, "input-payment-city")
    POST_CODE = (By.ID, "input-payment-postcode")
    COUNTRY = (By.ID, "input-payment-country")
    REGION = (By.ID, "input-payment-zone")
    
    # 배송 방법 및 결제 방법
    SHIPPING_METHOD = (By.NAME, "shipping_method")
    PAYMENT_METHOD = (By.NAME, "payment_method")
    AGREE_TERMS = (By.NAME, "agree")
    
    # 주문 확인
    CONFIRM_ORDER = (By.ID, "button-confirm")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "#content h1")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://demo.opencart.com/index.php?route=checkout/checkout"
        
    def select_guest_checkout(self):
        self.click_element(self.GUEST_CHECKOUT_RADIO)
        self.click_element(self.CONTINUE_BUTTON)
        
    def fill_personal_details(self, customer_data):
        self.input_text(self.FIRST_NAME, customer_data['firstname'])
        self.input_text(self.LAST_NAME, customer_data['lastname'])
        self.input_text(self.EMAIL, customer_data['email'])
        self.input_text(self.TELEPHONE, customer_data['telephone'])
        self.input_text(self.ADDRESS_1, customer_data['address'])
        self.input_text(self.CITY, customer_data['city'])
        self.input_text(self.POST_CODE, customer_data['postcode'])
        
        self.select_by_visible_text(self.COUNTRY, customer_data['country'])
        self.select_by_visible_text(self.REGION, customer_data['region'])
        
    def select_shipping_method(self):
        self.click_element(self.SHIPPING_METHOD)
        self.click_element(self.CONTINUE_BUTTON)
        
    def select_payment_method(self):
        self.click_element(self.PAYMENT_METHOD)
        self.click_element(self.AGREE_TERMS)
        self.click_element(self.CONTINUE_BUTTON)
        
    def confirm_order(self):
        self.click_element(self.CONFIRM_ORDER)
        
    def is_order_successful(self):
        success_text = self.get_text(self.SUCCESS_MESSAGE)
        return "Your order has been placed" in success_text 