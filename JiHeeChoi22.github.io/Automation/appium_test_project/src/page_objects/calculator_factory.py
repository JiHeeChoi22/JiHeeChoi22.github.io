from src.page_objects.android.calculator_page import CalculatorPage

class CalculatorFactory:
    @staticmethod
    def get_calculator(driver):
        """플랫폼에 맞는 계산기 페이지 객체 반환"""
        # 현재는 안드로이드만 지원
        return CalculatorPage(driver) 