from appium import webdriver
from appium.options.android import UiAutomator2Options
import json
import os
from src.utilities.logger import Logger

class DriverManager:
    def __init__(self):
        self.logger = Logger.get_logger()
        self.driver = None
        self.config = self._load_config()
    
    def _load_config(self):
        """설정 파일 로드"""
        try:
            config_path = os.path.join('configs', 'android_config.json')
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"설정 파일 로드 실패: {str(e)}")
            raise
    
    def init_driver(self):
        """Appium 드라이버 초기화"""
        try:
            options = UiAutomator2Options()
            
            # 설정 파일의 모든 capability 적용
            for key, value in self.config.items():
                if key != 'settings' and key != 'capabilities':
                    options.set_capability(key, value)
            
            # 추가 capabilities 적용
            if 'capabilities' in self.config:
                for key, value in self.config['capabilities'].items():
                    options.set_capability(key, value)
            
            # Appium 서버 연결
            self.driver = webdriver.Remote(
                command_executor='http://localhost:4723',
                options=options
            )
            
            # 설정 적용
            if 'settings' in self.config:
                for setting, value in self.config['settings'].items():
                    self.driver.update_settings({setting: value})
            
            self.logger.info("Appium 드라이버 초기화 성공")
            return self.driver
            
        except Exception as e:
            self.logger.error(f"드라이버 초기화 실패: {str(e)}")
            raise
    
    def quit_driver(self):
        """드라이버 종료"""
        try:
            if self.driver:
                self.driver.quit()
                self.logger.info("드라이버 종료 완료")
        except Exception as e:
            self.logger.error(f"드라이버 종료 실패: {str(e)}")
            raise 