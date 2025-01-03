import pytest
from datetime import datetime, UTC
from py.xml import html
import os

def pytest_configure(config):
    """테스트 리포트 메타데이터 설정"""
    config._metadata = {
        'Project': 'Calculator App Test',
        'Platform': os.getenv('TEST_PLATFORM', 'Android'),
        'Appium Version': '2.0'
    }

def pytest_html_report_title(report):
    """리포트 타이틀 설정"""
    report.title = "계산기 앱 테스트 결과"

def pytest_html_results_table_header(cells):
    """결과 테이블 헤더 커스터마이징"""
    cells.insert(2, html.th('Description'))
    cells.insert(1, html.th('Time', class_='sortable time', col='time'))
    cells.pop()

def pytest_html_results_table_row(report, cells):
    """결과 테이블 행 커스터마이징"""
    description = getattr(report, 'description', '')
    cells.insert(2, html.td(description))
    cells.insert(1, html.td(datetime.now(UTC), class_='col-time'))
    cells.pop()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """테스트 결과 처리"""
    outcome = yield
    report = outcome.get_result()
    
    if hasattr(item, 'function'):
        report.description = str(item.function.__doc__)
    
    if report.when == 'call' and report.failed:
        try:
            driver = item.funcargs['setup']
            driver = driver.driver
            screenshot_path = f"reports/screenshots/{item.name}.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            driver.save_screenshot(screenshot_path)
            
            if os.path.exists(screenshot_path):
                html = '<div><img src="%s" alt="screenshot" style="width:300px;height:200px" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screenshot_path
                report.extra = [pytest.html.extras.html(html)]
        except Exception as e:
            print(f"스크린샷 저장 실패: {e}") 