import pytest
from utilities.performance_helper import PerformanceHelper
from selenium.webdriver.common.by import By

class TestPerformance:
    @pytest.mark.performance
    def test_page_load_performance(self, driver):
        """
        페이지 로드 성능 테스트
        - 측정: 홈페이지 및 주요 페이지 로드 시간
        - 기준: 5초 이내 로드
        """
        perf = PerformanceHelper(driver)
        
        # 홈페이지 로드 시간 측정
        load_time = perf.measure_page_load_time("https://demo.opencart.com")
        assert load_time < 5, f"홈페이지 로드 시간이 너무 깁니다: {load_time}초"
        
        # 상품 목록 페이지 로드 시간 측정
        load_time = perf.measure_page_load_time("https://demo.opencart.com/index.php?route=product/category&path=20")
        assert load_time < 3, f"상품 목록 페이지 로드 시간이 너무 깁니다: {load_time}초"
        
        perf.save_metrics("page_load_test")
        
    @pytest.mark.performance
    def test_ui_response_performance(self, driver):
        """
        UI 응답 성능 테스트
        - 측정: 버튼 클릭, 입력 필드 응답 시간
        - 기준: 1초 이내 응답
        """
        perf = PerformanceHelper(driver)
        driver.get("https://demo.opencart.com/index.php?route=account/login")
        
        # 로그인 폼 응답 시간 측정
        response_time = perf.measure_element_response_time(
            (By.ID, "input-email"),
            "input"
        )
        assert response_time < 1, f"입력 필드 응답 시간이 너무 깁니다: {response_time}초"
        
        response_time = perf.measure_element_response_time(
            (By.CSS_SELECTOR, "button[type='submit']"),
            "click"
        )
        assert response_time < 0.5, f"버튼 응답 시간이 너무 깁니다: {response_time}초"
        
        perf.save_metrics("ui_response_test")
        
    @pytest.mark.performance
    def test_resource_usage(self, driver):
        """
        리소스 사용량 테스트
        - 측정: 메모리 사용량, 네트워크 요청
        - 기준: 메모리 1GB 이내, 요청 수 50개 이내
        """
        perf = PerformanceHelper(driver)
        driver.get("https://demo.opencart.com")
        
        metrics = perf.get_resource_metrics()
        
        if metrics['memory']:  # Chrome에서만 지원
            assert metrics['memory'] < 1024, \
                f"메모리 사용량이 너무 높습니다: {metrics['memory']}MB"
        
        assert len(metrics['resources']) < 50, \
            f"네트워크 요청이 너무 많습니다: {len(metrics['resources'])}개"
            
        perf.save_metrics("resource_usage_test") 