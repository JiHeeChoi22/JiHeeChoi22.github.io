from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utilities.logger import Logger

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = Logger.get_logger()
    
    def find_element(self, locator, timeout=10):
        """요소 찾기 with 명시적 대기"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.logger.debug(f"요소 찾음: {locator}")
            return element
        except Exception as e:
            self.logger.error(f"요소를 찾을 수 없음: {locator}, 에러: {str(e)}")
            raise
    
    def click_element(self, locator):
        """요소 클릭 with 대기"""
        try:
            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            self.logger.debug(f"요소 클릭: {locator}")
        except Exception as e:
            self.logger.error(f"요소 클릭 실패: {locator}, 에러: {str(e)}")
            raise
    
    def get_text(self, locator):
        """요소의 텍스트 가져오기"""
        try:
            element = self.find_element(locator)
            text = element.text
            self.logger.debug(f"텍스트 가져옴: {text} from {locator}")
            return text
        except Exception as e:
            self.logger.error(f"텍스트 가져오기 실패: {locator}, 에러: {str(e)}")
            raise 