import os
from dotenv import load_dotenv

class ConfigReader:
    def __init__(self):
        load_dotenv()
        self.browser_type = os.getenv('BROWSER_TYPE', 'chrome')
        self.base_url = os.getenv('BASE_URL', 'https://demo.opencart.com')
        self.implicit_wait = int(os.getenv('IMPLICIT_WAIT', '10'))

    def get_browser_type(self):
        return self.browser_type

    def get_base_url(self):
        return self.base_url

    def get_implicit_wait(self):
        return self.implicit_wait 