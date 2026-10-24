# agentic-web-scraper/src/driver_manager.py
from selenium import webdriver


class DriverManager:
    """
    Manages the setup and teardown of Selenium WebDriver instances.
    ลองใช้ Selenium Manager (มีใน selenium 4.6+) ก่อน ถ้าไม่ได้ค่อยใช้ webdriver-manager
    """

    def __init__(self, browser_name='chrome', headless=True):
        self.browser_name = browser_name.lower()
        self.headless = headless
        self.driver = None

    def _chrome(self):
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--log-level=3')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # ปิด log รก ๆ บน Windows
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36')
        try:
            return webdriver.Chrome(options=options)  # Selenium Manager หา driver ให้อัตโนมัติ
        except Exception as first_error:
            try:
                from selenium.webdriver.chrome.service import Service as ChromeService
                from webdriver_manager.chrome import ChromeDriverManager
                service = ChromeService(ChromeDriverManager().install())
                return webdriver.Chrome(service=service, options=options)
            except Exception as e:
                print(f"Error setting up Chrome driver: {first_error} / {e}")
                print("Make sure Google Chrome is installed.")
                return None

    def _firefox(self):
        options = webdriver.FirefoxOptions()
        if self.headless:
            options.add_argument('--headless')
        try:
            return webdriver.Firefox(options=options)
        except Exception as first_error:
            try:
                from selenium.webdriver.firefox.service import Service as FirefoxService
                from webdriver_manager.firefox import GeckoDriverManager
                service = FirefoxService(GeckoDriverManager().install())
                return webdriver.Firefox(service=service, options=options)
            except Exception as e:
                print(f"Error setting up Firefox driver: {first_error} / {e}")
                print("Make sure Mozilla Firefox is installed.")
                return None

    def get_driver(self):
        """Initializes and returns a WebDriver instance."""
        if self.driver:
            return self.driver

        if self.browser_name == 'chrome':
            self.driver = self._chrome()
        elif self.browser_name == 'firefox':
            self.driver = self._firefox()
        else:
            raise ValueError(f"Unsupported browser: {self.browser_name}. Choose 'chrome' or 'firefox'.")

        if self.driver:
            self.driver.implicitly_wait(5)
        return self.driver

    def quit_driver(self):
        """Quits the WebDriver instance if it's running."""
        if self.driver:
            self.driver.quit()
            self.driver = None
