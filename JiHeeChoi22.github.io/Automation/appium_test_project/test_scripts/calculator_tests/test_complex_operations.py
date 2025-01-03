import pytest
from utilities.driver_manager import DriverManager
from page_objects.calculator_page import CalculatorPage

@pytest.mark.regression
class TestComplexCalculations:
    """복잡한 계산기 기능 테스트"""
    @pytest.fixture(scope="function")
    def setup(self):
        self.driver_manager = DriverManager()
        self.driver = self.driver_manager.init_driver()
        self.calculator = CalculatorPage(self.driver)
        yield
        self.driver_manager.quit_driver()
    
    def test_multiple_operations(self, setup):
        """여러 연산자를 포함한 계산 테스트"""
        result = self.calculator.calculate("8*2+5")
        assert result == "21"
        
        result = self.calculator.calculate("15/3*4")
        assert result == "20"
    
    def test_large_numbers(self, setup):
        """큰 숫자 계산 테스트"""
        result = self.calculator.calculate("123+456")
        assert result == "579"
        
        result = self.calculator.calculate("999*999")
        assert result == "998001"
    
    def test_division_by_zero(self, setup):
        """0으로 나누기 테스트"""
        result = self.calculator.calculate("5/0")
        assert "Error" in result or "∞" in result
    
    def test_decimal_results(self, setup):
        """소수점 결과 테스트"""
        result = self.calculator.calculate("10/4")
        assert float(result) == 2.5
    
    @pytest.mark.parametrize("expression,expected", [
        ("5+5*2", "15"),
        ("20/4+7", "12"),
        ("8*4-6", "26"),
        ("100/10/2", "5")
    ])
    def test_operator_precedence(self, setup, expression, expected):
        """연산자 우선순위 테스트"""
        result = self.calculator.calculate(expression)
        assert result == expected 