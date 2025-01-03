import pytest
from src.utilities.logger import Logger
from src.utilities.test_data_loader import TestDataLoader

@pytest.mark.data_driven
class TestDataDrivenCalculator:
    """데이터 주도 계산기 테스트"""
    
    @pytest.fixture(scope="function")
    def setup(self):
        from src.utilities.driver_manager import DriverManager
        self.driver_manager = DriverManager()
        self.driver = self.driver_manager.init_driver()
        from src.page_objects.calculator_factory import CalculatorFactory
        self.calculator = CalculatorFactory.get_calculator(self.driver)
        yield
        self.driver_manager.quit_driver()
    
    @pytest.mark.parametrize(
        "test_data",
        TestDataLoader.get_test_cases("basic_operations"),
        ids=lambda x: x['description']
    )
    def test_basic_operations(self, setup, test_data):
        """기본 연산 테스트"""
        expression = test_data['expression']
        expected = test_data['expected']
        
        Logger.get_test_logger().info(f"테스트 시작: {test_data['description']}")
        result = self.calculator.calculate(expression)
        assert result == expected
    
    @pytest.mark.parametrize(
        "test_data",
        TestDataLoader.get_test_cases("complex_operations"),
        ids=lambda x: x['description']
    )
    def test_complex_operations(self, setup, test_data):
        """복잡한 연산 테스트"""
        expression = test_data['expression']
        expected = test_data['expected']
        
        Logger.get_test_logger().info(f"테스트 시작: {test_data['description']}")
        result = self.calculator.calculate(expression)
        assert result == expected
    
    @pytest.mark.parametrize(
        "test_data",
        TestDataLoader.get_test_cases("error_cases"),
        ids=lambda x: x['description']
    )
    def test_error_cases(self, setup, test_data):
        """에러 케이스 테스트"""
        expression = test_data['expression']
        
        Logger.get_test_logger().info(f"테스트 시작: {test_data['description']}")
        result = self.calculator.calculate_with_validation(expression)
        assert ("Error" in result or "∞" in result) == test_data['expected_error'] 