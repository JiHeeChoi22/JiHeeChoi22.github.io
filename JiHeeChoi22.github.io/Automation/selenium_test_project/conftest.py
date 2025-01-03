import pytest
from utilities.driver_factory import DriverFactory
from utilities.config_reader import ConfigReader
from datetime import datetime, UTC
import os
from py.xml import html
import logging

def pytest_addoption(parser):
    parser.addoption("--browser", 
                    action="store",
                    default="chrome",
                    help="브라우저 선택: chrome, firefox, edge")
    parser.addoption("--security-level",
                    action="store",
                    default="normal",
                    help="보안 테스트 수준: light, normal, strict")
    parser.addoption("--grid",
                    action="store_true",
                    help="Selenium Grid 사용 여부")

@pytest.fixture(scope="session")
def config():
    return ConfigReader()

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    use_grid = request.config.getoption("--grid")
    driver = DriverFactory.create_driver(browser, use_grid=use_grid)
    driver.maximize_window()
    
    def fin():
        driver.quit()
    
    request.addfinalizer(fin)
    return driver 

def pytest_configure(config):
    # 리포트 저장 디렉토리 생성
    if not os.path.exists('reports'):
        os.makedirs('reports')
        
    # 리포트에 추가할 메타데이터 설정
    config._metadata = {
        'Project Name': 'OpenCart Test Automation',
        'Tester': 'QA Team',
        'Environment': 'Test',
        'Browser': config.getoption('--browser')
    }

def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.insert(1, html.th('Time', class_='sortable time', col='time'))
    cells.insert(3, html.th('Type', class_='sortable', col='type'))
    cells.pop()

def pytest_html_results_table_row(report, cells):
    # 테스트 수집 단계에서는 description이 없을 수 있음
    description = getattr(report, 'description', '')
    cells.insert(2, html.td(description))
    cells.insert(1, html.td(datetime.now(UTC), class_='col-time'))
    # 테스트 유형 표시
    keywords = getattr(report, 'keywords', {})
    test_type = "보안" if "security" in keywords else \
                "성능" if "performance" in keywords else "기능"
    cells.insert(3, html.td(test_type, class_='col-type'))
    cells.pop()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    
    # 테스트 실패 시 스크린샷 첨부
    if report.when == "call" and report.failed:
        try:
            driver = item.funcargs['driver']
            take_screenshot(driver, item.name)
        except Exception as e:
            print(f"스크린샷 캡처 실패: {e}")

def take_screenshot(driver, name):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_dir = "reports/screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    screenshot_path = os.path.join(screenshot_dir, f"failure_{name}_{timestamp}.png")
    driver.save_screenshot(screenshot_path) 

def load_test_data(file_name):
    """CSV, JSON, YAML 등 다양한 포맷 지원"""
    # TODO: 구현 필요
    pass

# 로깅 설정
logging.basicConfig(
    filename='test_execution.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@pytest.fixture(autouse=True)
def retry_failed_tests():
    """실패한 테스트 자동 재시도"""
    return pytest.mark.flaky(reruns=3, reruns_delay=2) 