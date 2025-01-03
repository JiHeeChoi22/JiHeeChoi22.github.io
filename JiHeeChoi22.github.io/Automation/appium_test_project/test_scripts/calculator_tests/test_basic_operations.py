import pytest
from utilities.driver_manager import DriverManager
from page_objects.calculator_page import CalculatorPage
from page_objects.calculator_factory import CalculatorFactory

@pytest.mark.smoke
class TestCalculator:
    """기본 계산기 기능 테스트"""
    @pytest.fixture(scope="function")
    def setup(self):
        self.driver_manager = DriverManager()
        platform = 'android'  # 또는 환경변수/설정에서 가져오기
        self.driver = self.driver_manager.init_driver(platform)
        self.calculator = CalculatorFactory.get_calculator(self.driver, platform)
        yield
        self.driver_manager.quit_driver()
    
    def test_addition(self, setup):
        """덧셈 테스트"""
        result = self.calculator.calculate("5+3")
        assert result == "8"
    
    def test_subtraction(self, setup):
        """뺄셈 테스트"""
        result = self.calculator.calculate("9-4")
        assert result == "5"
    
    def test_multiplication(self, setup):
        """곱셈 테스트"""
        result = self.calculator.calculate("6*8")
        assert result == "48"
    
    def test_division(self, setup):
        """나눗셈 테스트"""
        result = self.calculator.calculate("15/3")
        assert result == "5"
    
    def test_clear_functionality(self, setup):
        """초기화 기능 테스트"""
        self.calculator.click_number(5)
        self.calculator.clear()
        result = self.calculator.get_result()
        assert result == "0" 