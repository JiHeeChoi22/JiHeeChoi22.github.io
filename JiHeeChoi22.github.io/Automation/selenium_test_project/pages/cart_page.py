from selenium.webdriver.common.by import By
from .base_page import BasePage

class CartPage(BasePage):
    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, ".table-responsive tbody tr")
    QUANTITY_INPUTS = (By.CSS_SELECTOR, "input[name^='quantity']")
    UPDATE_BUTTONS = (By.CSS_SELECTOR, "button[data-original-title='Update']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[data-original-title='Remove']")
    CART_TOTAL = (By.CSS_SELECTOR, "#content > div.row > div > table > tbody > tr:nth-child(4) > td:nth-child(2)")
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, "#content > p")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "a.btn-primary")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://demo.opencart.com/index.php?route=checkout/cart"
        
    def open(self):
        self.driver.get(self.url)
        
    def get_cart_items(self):
        return self.find_elements(self.CART_ITEMS)
        
    def update_quantity(self, product_index, quantity):
        quantity_inputs = self.find_elements(self.QUANTITY_INPUTS)
        update_buttons = self.find_elements(self.UPDATE_BUTTONS)
        
        if 0 <= product_index < len(quantity_inputs):
            self.input_text((By.CSS_SELECTOR, f"input[name^='quantity'][value]"), str(quantity))
            update_buttons[product_index].click()
            return True
        return False
        
    def remove_item(self, product_index):
        remove_buttons = self.find_elements(self.REMOVE_BUTTONS)
        if 0 <= product_index < len(remove_buttons):
            remove_buttons[product_index].click()
            return True
        return False
        
    def get_total_price(self):
        total_text = self.get_text(self.CART_TOTAL)
        return float(total_text.replace('$', '').replace(',', ''))
        
    def is_cart_empty(self):
        try:
            return "Your shopping cart is empty!" in self.get_text(self.EMPTY_CART_MESSAGE)
        except:
            return len(self.get_cart_items()) == 0
            
    def proceed_to_checkout(self):
        self.click_element(self.CHECKOUT_BUTTON) 