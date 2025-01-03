import pytest
from src.utilities.logger import Logger

@pytest.mark.basic
class TestNegativeNumbers:
    """음수 계산 테스트"""
    
    @pytest.fixture(scope="function")
    def setup(self):
        from src.utilities.driver_manager import DriverManager
        self.driver_manager = DriverManager()
        self.driver = self.driver_manager.init_driver()
        from src.page_objects.calculator_factory import CalculatorFactory
        self.calculator = CalculatorFactory.get_calculator(self.driver)
        yield
        self.driver_manager.quit_driver()
    
    def test_negative_addition(self, setup):
        """음수 덧셈 테스트"""
        result = self.calculator.calculate("-5+3")
        assert result == "-2"
    
    def test_negative_multiplication(self, setup):
        """음수 곱셈 테스트"""
        result = self.calculator.calculate("-4*3")
        assert result == "-12" 