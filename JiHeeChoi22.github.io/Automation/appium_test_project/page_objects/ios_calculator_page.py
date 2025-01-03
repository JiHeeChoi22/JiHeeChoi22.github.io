from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class IOSCalculatorPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
    # iOS 계산기 요소 접근자
    DIGIT_IDS = {
        '0': '0',
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5',
        '6': '6',
        '7': '7',
        '8': '8',
        '9': '9'
    }
    
    OPERATION_IDS = {
        '+': 'add',
        '-': 'subtract',
        '*': 'multiply',
        '/': 'divide'
    }
    
    EQUALS_BUTTON = 'equals'
    CLEAR_BUTTON = 'clear'
    RESULT_FIELD = 'result'
    DECIMAL_BUTTON = 'decimal'
    
    def _find_element(self, accessibility_id):
        """iOS 접근성 ID로 요소 찾기"""
        return self.wait.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, accessibility_id))
        )
    
    def click_number(self, number):
        """숫자 버튼 클릭"""
        self._find_element(self.DIGIT_IDS[str(number)]).click()
    
    def click_operation(self, operation):
        """연산자 버튼 클릭"""
        self._find_element(self.OPERATION_IDS[operation]).click()
    
    def click_equals(self):
        """등호 버튼 클릭"""
        self._find_element(self.EQUALS_BUTTON).click()
    
    def clear(self):
        """계산기 초기화"""
        self._find_element(self.CLEAR_BUTTON).click()
    
    def get_result(self):
        """결과값 반환"""
        result = self._find_element(self.RESULT_FIELD)
        return result.get_attribute('value')
    
    def click_decimal(self):
        """소수점 버튼 클릭"""
        self._find_element(self.DECIMAL_BUTTON).click()
    
    def calculate(self, expression):
        """수식 계산 (예: "5+3")"""
        self.clear()
        
        current_number = ''
        for char in expression:
            if char.isdigit():
                current_number += char
            elif char in self.OPERATION_IDS.keys():
                if current_number:
                    for digit in current_number:
                        self.click_number(digit)
                    current_number = ''
                self.click_operation(char)
            elif char == '.':
                if current_number:
                    for digit in current_number:
                        self.click_number(digit)
                    current_number = ''
                self.click_decimal()
        
        if current_number:
            for digit in current_number:
                self.click_number(digit)
                
        self.click_equals()
        return self.get_result() 