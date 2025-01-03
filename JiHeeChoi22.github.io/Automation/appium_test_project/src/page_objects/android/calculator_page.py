from appium.webdriver.common.appiumby import AppiumBy
from src.page_objects.base.base_page import BasePage
from src.utilities.logger import Logger

class CalculatorPage(BasePage):
    """안드로이드 계산기 페이지 객체"""
    
    # 요소 식별자
    DIGIT_IDS = {
        '0': 'com.android.calculator2:id/digit_0',
        '1': 'com.android.calculator2:id/digit_1',
        '2': 'com.android.calculator2:id/digit_2',
        '3': 'com.android.calculator2:id/digit_3',
        '4': 'com.android.calculator2:id/digit_4',
        '5': 'com.android.calculator2:id/digit_5',
        '6': 'com.android.calculator2:id/digit_6',
        '7': 'com.android.calculator2:id/digit_7',
        '8': 'com.android.calculator2:id/digit_8',
        '9': 'com.android.calculator2:id/digit_9'
    }
    
    OPERATION_IDS = {
        '+': 'com.android.calculator2:id/op_add',
        '-': 'com.android.calculator2:id/op_sub',
        '*': 'com.android.calculator2:id/op_mul',
        '/': 'com.android.calculator2:id/op_div'
    }
    
    # 기타 버튼
    EQUALS_BTN = (AppiumBy.ID, 'com.android.calculator2:id/eq')
    CLEAR_BTN = (AppiumBy.ID, 'com.android.calculator2:id/clr')
    RESULT_FIELD = (AppiumBy.ID, 'com.android.calculator2:id/result')
    
    # 메모리 버튼
    MEMORY_STORE = (AppiumBy.ID, 'com.android.calculator2:id/memory_store')
    MEMORY_RECALL = (AppiumBy.ID, 'com.android.calculator2:id/memory_recall')
    MEMORY_ADD = (AppiumBy.ID, 'com.android.calculator2:id/memory_add')
    
    def click_number(self, number):
        """숫자 버튼 클릭"""
        locator = (AppiumBy.ID, self.DIGIT_IDS[str(number)])
        self.click_element(locator)
        self.logger.debug(f"숫자 {number} 클릭")
    
    def click_operation(self, operation):
        """연산자 버튼 클릭"""
        locator = (AppiumBy.ID, self.OPERATION_IDS[operation])
        self.click_element(locator)
        self.logger.debug(f"연산자 {operation} 클릭")
    
    def click_equals(self):
        """= 버튼 클릭"""
        self.click_element(self.EQUALS_BTN)
        self.logger.debug("= 버튼 클릭")
    
    def clear(self):
        """C 버튼 클릭"""
        self.click_element(self.CLEAR_BTN)
        self.logger.debug("C 버튼 클릭")
    
    def get_result(self):
        """결과값 가져오기"""
        return self.get_text(self.RESULT_FIELD)
    
    def calculate(self, expression):
        """수식 계산 (예: "5+3")"""
        self.logger.info(f"수식 계산 시작: {expression}")
        try:
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
                elif char == '-' and not current_number:  # 음수 처리
                    self.click_operation('-')
            
            if current_number:
                for digit in current_number:
                    self.click_number(digit)
            
            self.click_equals()
            result = self.get_result()
            self.logger.info(f"계산 결과: {result}")
            return result
            
        except Exception as e:
            self.logger.error(f"계산 실패: {expression}, 에러: {str(e)}")
            raise
    
    def store_in_memory(self):
        """현재 값을 메모리에 저장"""
        self.click_element(self.MEMORY_STORE)
        self.logger.debug("메모리 저장")
    
    def recall_from_memory(self):
        """메모리에서 값 불러오기"""
        self.click_element(self.MEMORY_RECALL)
        self.logger.debug("메모리 불러오기")
    
    def add_to_memory(self):
        """현재 값을 메모리에 더하기"""
        self.click_element(self.MEMORY_ADD)
        self.logger.debug("메모리에 더하기") 