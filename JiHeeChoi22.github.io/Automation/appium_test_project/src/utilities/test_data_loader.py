import json
import os
from typing import Dict, List, Any

class TestDataLoader:
    _test_data = None

    @staticmethod
    def load_test_data() -> Dict[str, List[Dict[str, Any]]]:
        """테스트 데이터 로드"""
        if TestDataLoader._test_data is None:
            data_file = os.path.join('tests', 'data', 'calculator_test_data.json')
            with open(data_file, 'r', encoding='utf-8') as f:
                TestDataLoader._test_data = json.load(f)
        return TestDataLoader._test_data

    @staticmethod
    def get_test_cases(category: str) -> List[Dict[str, Any]]:
        """특정 카테고리의 테스트 케이스 반환"""
        data = TestDataLoader.load_test_data()
        return data.get(category, []) 