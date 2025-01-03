import pytest
from datetime import datetime, UTC
from py.xml import html
import os

def pytest_configure(config):
    """테스트 리포트 메타데이터 설정"""
    # 메타데이터 초기화
    metadata = getattr(config, '_metadata', {})
    metadata['Project'] = 'Calculator App Test'
    metadata['Platform'] = os.getenv('TEST_PLATFORM', 'Android')
    metadata['Appium Version'] = '2.0'
    setattr(config, '_metadata', metadata)

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
    # CollectReport인 경우 description 속성이 없을 수 있음
    description = getattr(report, 'description', '')
    cells.insert(2, html.td(description))
    cells.insert(1, html.td(datetime.now(UTC), class_='col-time'))
    cells.pop()

def pytest_html_results_summary(prefix, summary, postfix):
    """테스트 요약 정보 추가"""
    prefix.extend([html.p("테스트 환경:")])
    for key, value in summary.items():
        prefix.extend([html.p(f"{key}: {value}")])

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """테스트 결과 처리"""
    outcome = yield
    report = outcome.get_result()
    
    # 테스트 함수에 docstring이 있는 경우에만 description 설정
    if hasattr(item, 'function'):
        report.description = str(item.function.__doc__)
    
    # 스크린샷 첨부 (실패한 경우)
    if report.when == 'call' and report.failed:
        try:
            driver = item.funcargs['setup']
            driver = driver.driver  # DriverManager 인스턴스에서 실제 드라이버 가져오기
            screenshot_path = f"reports/screenshots/{item.name}.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            driver.save_screenshot(screenshot_path)
            
            if os.path.exists(screenshot_path):
                html = '<div><img src="%s" alt="screenshot" style="width:300px;height:200px" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screenshot_path
                report.extra = [pytest.html.extras.html(html)]
        except Exception as e:
            print(f"스크린샷 저장 실패: {e}") 