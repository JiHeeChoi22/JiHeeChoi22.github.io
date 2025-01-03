from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager, ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from utilities.grid_helper import GridHelper
import os
import platform

class DriverFactory:
    @staticmethod
    def create_driver(browser_type="chrome", options=None, use_grid=False):
        browser_type = browser_type.lower()
        
        if use_grid:
            grid = GridHelper()
            return grid.create_remote_driver(browser_type, options)
        
        if browser_type == "chrome":
            chrome_options = ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            if options:
                for option in options:
                    chrome_options.add_argument(option)
            try:
                chrome_manager = ChromeDriverManager().install()
                return webdriver.Chrome(
                    service=ChromeService(chrome_manager),
                    options=chrome_options
                )
            except Exception as e:
                print(f"ChromeDriver 초기화 실패: {e}")
                print("Chrome 초기화 실패. Edge로 전환합니다.")
                return DriverFactory.create_driver("edge", options)
            
        elif browser_type == "firefox":
            firefox_options = FirefoxOptions()
            if platform.system() == 'Windows':
                paths = [
                    r"C:\Program Files\Mozilla Firefox\firefox.exe",
                    r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
                    os.getenv('PROGRAMFILES') + r"\Mozilla Firefox\firefox.exe",
                    os.getenv('PROGRAMFILES(X86)') + r"\Mozilla Firefox\firefox.exe"
                ]
                for path in paths:
                    if os.path.exists(path):
                        firefox_options.binary_location = path
                        break
            if options:
                for option in options:
                    firefox_options.add_argument(option)
            try:
                return webdriver.Firefox(
                    service=FirefoxService(GeckoDriverManager().install()),
                    options=firefox_options
                )
            except Exception as e:
                print(f"Firefox 초기화 실패: {e}")
                print("Firefox 초기화 실패. Edge로 전환합니다.")
                return DriverFactory.create_driver("edge", options)
            
        elif browser_type == "edge":
            edge_options = EdgeOptions()
            if options:
                for option in options:
                    edge_options.add_argument(option)
            return webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),
                options=edge_options
            )
            
        else:
            raise ValueError(f"지원하지 않는 브라우저 타입: {browser_type}") 