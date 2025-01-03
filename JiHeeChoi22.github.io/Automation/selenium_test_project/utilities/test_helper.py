import logging
import os
from datetime import datetime

class TestHelper:
    @staticmethod
    def take_screenshot(driver, name):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_name = f"{name}_{timestamp}.png"
        screenshot_dir = "screenshots"
        
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
            
        driver.save_screenshot(os.path.join(screenshot_dir, screenshot_name))
        
    @staticmethod
    def setup_logging():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('test_execution.log'),
                logging.StreamHandler()
            ]
        ) 