from selenium.webdriver.common.by import By
from .base_page import BasePage

class SearchPage(BasePage):
    # Locators
    SEARCH_INPUT = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".btn-default[type='button']")
    CATEGORY_DROPDOWN = (By.NAME, "category_id")
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".product-layout")
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".product-layout .caption h4 a")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, "#content > p")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://demo.opencart.com/index.php?route=product/search"
        
    def open(self):
        self.driver.get(self.url)
        
    def search_product(self, keyword, category=None):
        self.input_text(self.SEARCH_INPUT, keyword)
        
        if category:
            self.select_category(category)
            
        self.click_element(self.SEARCH_BUTTON)
        
    def select_category(self, category_name):
        self.select_by_visible_text(self.CATEGORY_DROPDOWN, category_name)
        
    def get_search_results(self):
        return self.find_elements(self.SEARCH_RESULTS)
        
    def get_product_titles(self):
        elements = self.find_elements(self.PRODUCT_TITLES)
        return [element.text for element in elements]
        
    def is_product_found(self, product_name):
        titles = self.get_product_titles()
        return any(product_name.lower() in title.lower() for title in titles)
        
    def get_no_results_message(self):
        return self.get_text(self.NO_RESULTS_MESSAGE) 