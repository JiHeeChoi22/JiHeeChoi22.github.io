from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
import json
import os

class DriverManager:
    def __init__(self):
        self.driver = None
        
    def init_driver(self, platform='android'):
        config_path = os.path.join('configs', f'{platform}_config.json')
        
        with open(config_path) as f:
            capabilities = json.load(f)
        
        # 플랫폼별 Options 객체 생성
        if platform.lower() == 'android':
            options = UiAutomator2Options()
        else:
            options = XCUITestOptions()
            
        # capabilities를 options에 설정
        for key, value in capabilities.items():
            options.set_capability(key, value)
        
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4723',
            options=options
        )
        return self.driver
        
    def quit_driver(self):
        if self.driver:
            self.driver.quit() 