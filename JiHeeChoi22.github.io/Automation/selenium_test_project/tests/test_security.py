import pytest
from utilities.security_helper import SecurityHelper
from selenium.webdriver.common.by import By

class TestSecurity:
    @pytest.mark.security
    def test_xss_vulnerability(self, driver):
        """
        XSS 취약점 테스트
        - 검증: 악성 스크립트 실행 차단
        """
        security = SecurityHelper(driver)
        
        # 검색창 XSS 테스트
        xss_payload = "<script>window.xssTestPassed = true;</script>"
        result = security.test_xss_payload(
            (By.NAME, "search"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            xss_payload
        )
        
        assert result, "XSS 취약점이 발견되었습니다"
        
    @pytest.mark.security
    def test_sql_injection(self, driver):
        """
        SQL 인젝션 취약점 테스트
        - 검증: SQL 인젝션 공격 차단
        """
        security = SecurityHelper(driver)
        
        # 로그인 폼 SQL 인젝션 테스트
        test_url = "https://demo.opencart.com/index.php?route=account/login"
        test_params = {
            "username": "' OR '1'='1",
            "password": "' OR '1'='1"
        }
        
        result = security.test_sql_injection(test_url, test_params)
        assert result, "SQL 인젝션 취약점이 발견되었습니다"
        
    @pytest.mark.security
    def test_csrf_protection(self, driver):
        """
        CSRF 보호 테스트
        - 검증: CSRF 토큰 검증
        """
        security = SecurityHelper(driver)
        
        # 장바구니 추가 CSRF 테스트
        test_url = "https://demo.opencart.com/index.php?route=checkout/cart/add"
        result = security.test_csrf_protection(test_url)
        
        assert result, "CSRF 보호가 충분하지 않습니다"
        
    @pytest.mark.security
    def test_security_headers(self, driver):
        """
        보안 헤더 테스트
        - 검증: 필수 보안 헤더 존재 여부
        """
        security = SecurityHelper(driver)
        driver.get("https://demo.opencart.com")
        
        headers = security.test_secure_headers()
        
        # 필수 보안 헤더 확인
        assert headers['X-Frame-Options'], "X-Frame-Options 헤더가 없습니다"
        assert headers['X-XSS-Protection'], "X-XSS-Protection 헤더가 없습니다"
        assert headers['X-Content-Type-Options'], "X-Content-Type-Options 헤더가 없습니다" 