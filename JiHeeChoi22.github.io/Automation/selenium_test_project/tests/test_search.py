import pytest
from pages.search_page import SearchPage
from utilities.test_data_loader import read_test_data
from utilities.test_retry import TestRetry

class TestSearch:
    @pytest.mark.parametrize("test_data", read_test_data("search_data.csv"))
    @TestRetry.retry_test(max_attempts=3)
    def test_product_search(self, driver, test_data):
        """
        상품 검색 기능 테스트
        - 데이터: CSV 파일의 키워드와 카테고리 조합
        - 검증: 검색 결과 수량 및 일치하는 상품 확인
        """
        search_page = SearchPage(driver)
        search_page.open()
        
        search_page.search_product(
            test_data['keyword'],
            test_data.get('category')
        )
        
        if test_data['expected_result'] == 'success':
            results = search_page.get_search_results()
            assert len(results) == int(test_data['expected_count']), \
                f"Expected {test_data['expected_count']} results, but got {len(results)}"
            
            if test_data['keyword']:
                assert search_page.is_product_found(test_data['keyword']), \
                    f"Product with keyword '{test_data['keyword']}' not found in search results"
        else:
            assert "There is no product that matches the search criteria" in \
                search_page.get_no_results_message()

    def test_search_with_partial_match(self, driver):
        """
        부분 일치 검색 테스트
        - 검증: 검색어를 포함하는 모든 상품 표시 확인
        """
        search_page = SearchPage(driver)
        search_page.open()
        
        partial_keyword = "phone"
        search_page.search_product(partial_keyword)
        
        results = search_page.get_product_titles()
        assert any(partial_keyword.lower() in title.lower() for title in results), \
            f"No products found containing '{partial_keyword}'"

    def test_search_with_filters(self, driver):
        search_page = SearchPage(driver)
        search_page.open()
        
        search_page.search_product("mac", "Laptops & Notebooks")
        results = search_page.get_search_results()
        
        assert len(results) > 0, "No results found with category filter"
        assert all("mac" in title.lower() for title in search_page.get_product_titles()), \
            "Some results don't match the search criteria" 