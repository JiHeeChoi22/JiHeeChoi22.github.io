import pytest
from src.utilities.logger import Logger

@pytest.mark.boundary
class TestBoundaryCases:
    """경계값 테스트"""
    
    @pytest.fixture(scope="function")
    def setup(self):
        from src.utilities.driver_manager import DriverManager
        self.driver_manager = DriverManager()
        self.driver = self.driver_manager.init_driver()
        from src.page_objects.calculator_factory import CalculatorFactory
        self.calculator = CalculatorFactory.get_calculator(self.driver)
        yield
        self.driver_manager.quit_driver()
    
    def test_large_numbers(self, setup):
        """큰 숫자 계산 테스트"""
        result = self.calculator.calculate("999999*999999")
        assert len(result) <= 10  # 결과가 최대 자릿수를 초과하지 않아야 함 