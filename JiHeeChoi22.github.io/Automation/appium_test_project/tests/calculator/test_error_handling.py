import pytest
from src.utilities.logger import Logger

@pytest.mark.error
class TestErrorHandling:
    """에러 처리 테스트"""
    
    @pytest.fixture(scope="function")
    def setup(self):
        from src.utilities.driver_manager import DriverManager
        self.driver_manager = DriverManager()
        self.driver = self.driver_manager.init_driver()
        from src.page_objects.calculator_factory import CalculatorFactory
        self.calculator = CalculatorFactory.get_calculator(self.driver)
        yield
        self.driver_manager.quit_driver()
    
    def test_division_by_zero(self, setup):
        """0으로 나누기 테스트"""
        result = self.calculator.calculate("5/0")
        assert "Error" in result or "∞" in result
    
    def test_invalid_input(self, setup):
        """잘못된 입력 테스트"""
        result = self.calculator.calculate("2++2")
        assert "Error" in result 