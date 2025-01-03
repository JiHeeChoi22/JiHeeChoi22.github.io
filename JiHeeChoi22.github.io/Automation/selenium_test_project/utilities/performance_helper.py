import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import json
import os

class PerformanceHelper:
    def __init__(self, driver):
        self.driver = driver
        self.metrics = {}
        
    def measure_page_load_time(self, url):
        """페이지 로드 시간 측정"""
        start_time = time.time()
        self.driver.get(url)
        
        # document.readyState가 'complete'가 될 때까지 대기
        WebDriverWait(self.driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        end_time = time.time()
        load_time = end_time - start_time
        
        self.metrics['page_load_time'] = load_time
        return load_time
        
    def measure_element_response_time(self, locator, action):
        """UI 응답 시간 측정"""
        start_time = time.time()
        
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )
        
        if action == "click":
            element.click()
        elif action == "input":
            element.send_keys("test")
            
        end_time = time.time()
        response_time = end_time - start_time
        
        if 'element_response_times' not in self.metrics:
            self.metrics['element_response_times'] = []
        
        self.metrics['element_response_times'].append({
            'locator': str(locator),
            'action': action,
            'response_time': response_time
        })
        
        return response_time
        
    def get_resource_metrics(self):
        """리소스 사용량 측정"""
        # 페이지 로드 완료 대기
        WebDriverWait(self.driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        # 잠시 대기하여 모든 리소스가 로드되도록 함
        time.sleep(2)
        
        metrics = self.driver.execute_script("""
            return {
                'memory': performance.memory ? performance.memory.usedJSHeapSize / (1024 * 1024) : null,
                'navigation': performance.getEntriesByType('navigation')[0],
                'resources': performance.getEntriesByType('resource')
            }
        """)
        
        self.metrics['resource_metrics'] = metrics
        return metrics
        
    def save_metrics(self, test_name):
        """성능 메트릭을 JSON 파일로 저장"""
        if not os.path.exists('reports/performance'):
            os.makedirs('reports/performance')
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"reports/performance/{test_name}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.metrics, f, indent=2) 