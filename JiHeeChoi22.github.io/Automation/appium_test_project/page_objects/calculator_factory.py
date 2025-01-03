from page_objects.calculator_page import CalculatorPage
from page_objects.ios_calculator_page import IOSCalculatorPage

class CalculatorFactory:
    @staticmethod
    def get_calculator(driver, platform='android'):
        """플랫폼에 맞는 계산기 Page Object 반환"""
        if platform.lower() == 'ios':
            return IOSCalculatorPage(driver)
        return CalculatorPage(driver) 