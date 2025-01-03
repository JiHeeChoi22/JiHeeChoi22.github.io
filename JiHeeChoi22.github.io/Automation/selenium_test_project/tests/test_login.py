import pytest
from pages.login_page import LoginPage
from utilities.test_data_loader import read_test_data
from utilities.test_retry import TestRetry

class TestLogin:
    @pytest.mark.parametrize("test_data", read_test_data("login_data.csv"))
    @TestRetry.retry_test(max_attempts=3)
    def test_login(self, driver, test_data):
        """
        로그인 기능 테스트
        - 데이터: CSV 파일에서 읽은 테스트 데이터 사용
        - 검증: 로그인 성공/실패 여부 및 에러 메시지 확인
        """
        login_page = LoginPage(driver)
        login_page.open()
        
        login_page.login(
            test_data['username'],
            test_data['password']
        )
        
        if test_data['expected_result'] == 'success':
            assert login_page.is_login_successful()
        else:
            assert login_page.get_error_message() == test_data['error_message'] 