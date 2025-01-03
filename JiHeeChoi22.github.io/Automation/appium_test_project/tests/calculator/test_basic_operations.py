import pytest
from src.utilities.logger import Logger
from src.page_objects.calculator_factory import CalculatorFactory

@pytest.mark.basic
class TestBasicOperations:
    """기본 계산기 기능 테스트"""
    
    @pytest.fixture(scope="function")
    def setup(self):
        from src.utilities.driver_manager import DriverManager
        self.driver_manager = DriverManager()
        self.driver = self.driver_manager.init_driver()
        self.calculator = CalculatorFactory.get_calculator(self.driver)
        yield
        self.driver_manager.quit_driver()
    
    @Logger.log_test_step("기본 덧셈 연산")
    def test_addition(self, setup):
        """덧셈 테스트"""
        result = self.calculator.calculate("5+3")
        assert result == "8"
        
    @Logger.log_test_step("기본 뺄셈 연산")
    def test_subtraction(self, setup):
        """뺄셈 테스트"""
        result = self.calculator.calculate("9-4")
        assert result == "5" 