import pytest
from src.utilities.logger import Logger

@pytest.mark.memory
class TestMemoryFunctions:
    """메모리 기능 테스트"""
    
    @pytest.fixture(scope="function")
    def setup(self):
        from src.utilities.driver_manager import DriverManager
        self.driver_manager = DriverManager()
        self.driver = self.driver_manager.init_driver()
        from src.page_objects.calculator_factory import CalculatorFactory
        self.calculator = CalculatorFactory.get_calculator(self.driver)
        yield
        self.driver_manager.quit_driver()
    
    def test_memory_store_recall(self, setup):
        """메모리 저장 및 불러오기 테스트"""
        self.calculator.calculate("5")
        self.calculator.store_in_memory()
        self.calculator.clear()
        self.calculator.recall_from_memory()
        result = self.calculator.get_result()
        assert result == "5"
    
    def test_memory_add(self, setup):
        """메모리 더하기 테스트"""
        self.calculator.calculate("5")
        self.calculator.store_in_memory()
        self.calculator.calculate("3")
        self.calculator.add_to_memory()
        self.calculator.recall_from_memory()
        result = self.calculator.get_result()
        assert result == "8" 