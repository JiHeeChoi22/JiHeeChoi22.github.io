from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging

class GridHelper:
    def __init__(self, hub_url="http://localhost:4444/wd/hub"):
        self.hub_url = hub_url
        self.logger = logging.getLogger(__name__)
        
    def create_remote_driver(self, browser_type="chrome", options=None):
        """Selenium Grid 원격 드라이버 생성"""
        try:
            if browser_type == "chrome":
                capabilities = DesiredCapabilities.CHROME.copy()
                if options:
                    capabilities.update(options)
                    
            elif browser_type == "firefox":
                capabilities = DesiredCapabilities.FIREFOX.copy()
                if options:
                    capabilities.update(options)
                    
            else:
                raise ValueError(f"지원하지 않는 브라우저 타입: {browser_type}")
                
            driver = webdriver.Remote(
                command_executor=self.hub_url,
                desired_capabilities=capabilities
            )
            
            self.logger.info(f"원격 {browser_type} 드라이버 생성 성공")
            return driver
            
        except Exception as e:
            self.logger.error(f"원격 드라이버 생성 실패: {e}")
            raise
            
    def get_grid_status(self):
        """Grid 노드 상태 확인"""
        try:
            response = requests.get(f"{self.hub_url}/status")
            return response.json()
        except Exception as e:
            self.logger.error(f"Grid 상태 확인 실패: {e}")
            return None 