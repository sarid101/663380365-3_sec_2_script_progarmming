# agentic-web-scraper/src/scraper_agent.py
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException, StaleElementReferenceException,
                                        TimeoutException)

from .driver_manager import DriverManager
from .data_models import Product
from .utils import wait_for_element, robust_click, save_data_to_json

logger = logging.getLogger(__name__)


class ScraperAgent:
    """
    An agentic web scraper that operates based on a provided configuration.
    Perceive (อ่านหน้าเว็บ) -> Act (ดึงข้อมูล / คลิก Next) -> วนจนจบตามเป้าหมายใน config
    """

    def __init__(self, config, browser='chrome', headless=True):
        self.config = config
        self.driver_manager = DriverManager(browser_name=browser, headless=headless)
        self.driver = None
        self.scraped_products = []
        self.max_pages = config.get("max_pages", 5)

    # ---------- helpers ----------
    @staticmethod
    def _by(selector):
        """เดาว่าเป็น XPath หรือ CSS จากรูปแบบของ selector"""
        return By.XPATH if selector.startswith(("/", "(")) else By.CSS_SELECTOR

    def _find(self, parent, selector):
        if not selector:
            return None
        try:
            return parent.find_element(self._by(selector), selector)
        except (NoSuchElementException, StaleElementReferenceException):
            return None

    def _get_text(self, parent, selector):
        el = self._find(parent, selector)
        return el.text.strip() if el else None

    def _get_attr(self, parent, selector, attribute):
        el = self._find(parent, selector)
        if not el:
            return None
        value = el.get_attribute(attribute)  # href/src จะได้เป็น URL เต็มอัตโนมัติ
        return value.strip() if value else None

    # ---------- perception / action ----------
    def _parse_product_data(self, item):
        s = self.config["item_data_selectors"]
        name = self._get_text(item, s.get("name"))
        price = self._get_text(item, s.get("price"))
        if not (name and price):
            return None
        return Product(
            name=name,
            price=price,
            description=self._get_text(item, s.get("description")),
            url=self._get_attr(item, s.get("url"), "href"),
            image_url=self._get_attr(item, s.get("image_url"), "src"),
        )

    def scrape_page(self):
        """Scrapes all product items from the current page."""
        selector = self.config["item_container_selector"]
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((self._by(selector), selector)))
        except TimeoutException:
            logger.warning(f"No items found with selector '{selector}'")
            return 0

        count = 0
        for item in self.driver.find_elements(self._by(selector), selector):
            product = self._parse_product_data(item)
            if product:
                self.scraped_products.append(product.to_dict())
                count += 1
        return count

    def _go_next_page(self):
        """Finds and clicks the 'next page' link. Returns True if moved to a new page."""
        selector = self.config.get("pagination_selector")
        if not selector:
            return False
        if not wait_for_element(self.driver, self._by(selector), selector, timeout=5):
            return False  # หน้าสุดท้ายแล้ว
        old_url = self.driver.current_url
        if not robust_click(self.driver, self._by(selector), selector):
            return False
        try:
            WebDriverWait(self.driver, 10).until(EC.url_changes(old_url))
        except TimeoutException:
            return False
        return True

    def run(self):
        """Executes the scraping loop."""
        self.driver = self.driver_manager.get_driver()
        if not self.driver:
            print("Failed to get WebDriver. Exiting.")
            return

        try:
            self.driver.get(self.config["start_url"])
            current_page = 1
            while current_page <= self.max_pages:
                print(f"Scraping page {current_page}...")
                self.scrape_page()

                if current_page == self.max_pages:
                    break
                time.sleep(self.config.get("delay_between_pages", 2))  # สุภาพกับเว็บไซต์
                if not self._go_next_page():
                    break
                current_page += 1
        except Exception as e:
            print(f"An unhandled error occurred during scraping: {e}")
        finally:
            self.driver_manager.quit_driver()
            path = save_data_to_json(self.scraped_products, "scraped_products.json")
            if path:
                print(f"Successfully scraped {len(self.scraped_products)} items and saved to {path}")
