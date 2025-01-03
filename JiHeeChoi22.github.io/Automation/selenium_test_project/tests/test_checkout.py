import pytest
from pages.checkout_page import CheckoutPage
from pages.cart_page import CartPage
from pages.search_page import SearchPage
from utilities.test_data_loader import read_test_data
from utilities.test_retry import TestRetry

class TestCheckout:
    @pytest.fixture
    def setup_cart(self, driver):
        # 장바구니에 상품 추가
        search_page = SearchPage(driver)
        search_page.open()
        search_page.search_product("iPhone")
        
        cart_page = CartPage(driver)
        cart_page.open()
        if cart_page.is_cart_empty():
            pytest.skip("장바구니가 비어있어 체크아웃을 진행할 수 없습니다.")
    
    @pytest.mark.usefixtures("setup_cart")
    @TestRetry.retry_test(max_attempts=3)
    def test_guest_checkout(self, driver):
        """
        게스트 체크아웃 프로세스 테스트
        - 전제조건: 장바구니에 상품 있음
        - 검증: 주문 완료 확인
        """
        checkout_page = CheckoutPage(driver)
        checkout_page.open()
        
        # 테스트 데이터 로드
        test_data = read_test_data("checkout_data.json")
        
        # 게스트 체크아웃 진행
        checkout_page.select_guest_checkout()
        checkout_page.fill_personal_details(test_data['customer'])
        checkout_page.select_shipping_method()
        checkout_page.select_payment_method()
        checkout_page.confirm_order()
        
        # 주문 성공 확인
        assert checkout_page.is_order_successful(), "주문 처리에 실패했습니다."
    
    def test_required_fields_validation(self, driver):
        """
        체크아웃 필수 필드 검증 테스트
        - 검증: 필수 입력 필드 누락 시 에러 메시지 표시
        """
        checkout_page = CheckoutPage(driver)
        checkout_page.open()
        
        # 필수 필드를 비워두고 진행
        checkout_page.select_guest_checkout()
        checkout_page.click_element(checkout_page.CONTINUE_BUTTON)
        
        # 에러 메시지 확인
        assert checkout_page.is_element_visible((By.CLASS_NAME, "text-danger")), \
            "필수 필드 검증 에러가 표시되지 않았습니다."
    
    def test_shipping_method_selection(self, driver):
        checkout_page = CheckoutPage(driver)
        checkout_page.open()
        
        test_data = read_test_data("checkout_data.json")
        checkout_page.select_guest_checkout()
        checkout_page.fill_personal_details(test_data['customer'])
        
        # 배송 방법 선택 확인
        checkout_page.select_shipping_method()
        assert checkout_page.is_element_visible(checkout_page.PAYMENT_METHOD), \
            "배송 방법 선택 후 결제 방법 선택 화면으로 이동하지 않았습니다." 