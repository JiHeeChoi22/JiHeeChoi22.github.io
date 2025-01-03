import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class SecurityHelper:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        
    def test_xss_payload(self, input_locator, submit_locator, payload):
        """XSS 취약점 테스트"""
        try:
            input_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(input_locator)
            )
            input_element.clear()
            input_element.send_keys(payload)
            
            submit_button = self.driver.find_element(*submit_locator)
            submit_button.click()
            
            # XSS 스크립트 실행 여부 확인
            result = self.driver.execute_script("return window.xssTestPassed")
            return result is None  # None이면 스크립트가 실행되지 않음 (안전)
            
        except Exception as e:
            self.logger.error(f"XSS 테스트 실패: {e}")
            return False
            
    def test_sql_injection(self, url, params):
        """SQL 인젝션 취약점 테스트"""
        try:
            # SQL 인젝션 페이로드로 요청
            response = requests.get(url, params=params)
            
            # 의심스러운 응답 패턴 확인
            suspicious_patterns = [
                "SQL syntax",
                "mysql_fetch_array",
                "ORA-01756",
                "SQLServer JDBC Driver"
            ]
            
            return not any(pattern in response.text for pattern in suspicious_patterns)
            
        except Exception as e:
            self.logger.error(f"SQL 인젝션 테스트 실패: {e}")
            return False
            
    def test_csrf_protection(self, url, method="POST", data=None):
        """CSRF 보호 테스트"""
        try:
            # CSRF 토큰 없이 요청
            response = requests.request(method, url, data=data)
            
            # 보호가 있다면 403 또는 토큰 관련 에러가 발생해야 함
            return response.status_code in [403, 401] or "csrf" in response.text.lower()
            
        except Exception as e:
            self.logger.error(f"CSRF 보호 테스트 실패: {e}")
            return False
            
    def test_secure_headers(self):
        """보안 헤더 테스트"""
        current_url = self.driver.current_url
        response = requests.get(current_url)
        headers = response.headers
        
        security_headers = {
            'X-Frame-Options': False,
            'X-XSS-Protection': False,
            'X-Content-Type-Options': False,
            'Strict-Transport-Security': False,
            'Content-Security-Policy': False
        }
        
        for header in security_headers.keys():
            if header in headers:
                security_headers[header] = True
                
        return security_headers 