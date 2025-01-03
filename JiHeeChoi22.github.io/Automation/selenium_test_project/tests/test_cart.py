import pytest
from pages.cart_page import CartPage
from pages.search_page import SearchPage
from utilities.test_data_loader import read_test_data
from utilities.test_retry import TestRetry

class TestCart:
    @pytest.mark.parametrize("test_data", read_test_data("cart_data.csv"))
    @TestRetry.retry_test(max_attempts=3)
    def test_add_to_cart(self, driver, test_data):
        """
        장바구니 추가 및 수량 변경 테스트
        - 데이터: CSV 파일의 상품 정보와 수량
        - 검증: 장바구니 합계 금액 확인
        """
        # 상품 검색 및 장바구니 추가
        search_page = SearchPage(driver)
        search_page.open()
        search_page.search_product(test_data['product_name'])
        
        # 장바구니 수량 업데이트
        cart_page = CartPage(driver)
        cart_page.open()
        cart_page.update_quantity(0, int(test_data['quantity']))
        
        # 총액 검증
        assert cart_page.get_total_price() == float(test_data['expected_total']), \
            f"Cart total does not match expected amount"

    def test_remove_from_cart(self, driver):
        """
        장바구니 상품 제거 테스트
        - 검증: 상품 제거 후 장바구니 비어있음 확인
        """
        cart_page = CartPage(driver)
        cart_page.open()
        
        if not cart_page.is_cart_empty():
            cart_page.remove_item(0)
            assert len(cart_page.get_cart_items()) == 0, \
                "Item was not removed from cart"

    def test_cart_persistence(self, driver):
        # 장바구니에 상품 추가
        search_page = SearchPage(driver)
        search_page.open()
        search_page.search_product("iPhone")
        
        # 브라우저 새로고침 후 장바구니 확인
        driver.refresh()
        cart_page = CartPage(driver)
        cart_page.open()
        
        assert not cart_page.is_cart_empty(), \
            "Cart items were not persisted after page refresh"

    def test_proceed_to_checkout(self, driver):
        cart_page = CartPage(driver)
        cart_page.open()
        
        if not cart_page.is_cart_empty():
            cart_page.proceed_to_checkout()
            assert "checkout" in driver.current_url, \
                "Failed to proceed to checkout" 