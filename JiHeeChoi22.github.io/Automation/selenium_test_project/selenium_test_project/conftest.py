def pytest_configure(config):
    # 기존 코드
    # config._metadata['Project Name'] = 'OpenCart Test Automation'
    config.setoption('project_name', 'OpenCart Test Automation')  # 수정된 부분