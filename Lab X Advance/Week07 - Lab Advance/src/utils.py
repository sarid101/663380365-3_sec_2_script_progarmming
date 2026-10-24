# agentic-web-scraper/src/utils.py
import os
import time
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


def save_data_to_json(data, filename, directory='data'):
    """Saves a list of dictionaries to a JSON file. Returns the file path (or None)."""
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return filepath
    except IOError as e:
        print(f"Error saving data to JSON file: {e}")
        return None


def wait_for_element(driver, by, value, timeout=10):
    """Waits until an element is visible. Returns the element or None."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
    except TimeoutException:
        return None


def robust_click(driver, by, value, max_attempts=3, delay_between_attempts=2):
    """Attempts to click an element multiple times (retry mechanism)."""
    for attempt in range(max_attempts):
        try:
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, value)))
            element.click()
            return True
        except (TimeoutException, WebDriverException) as e:
            print(f"Click attempt {attempt + 1} failed: {type(e).__name__}")
            if attempt < max_attempts - 1:
                time.sleep(delay_between_attempts)
    print(f"Failed to click element {value} after {max_attempts} attempts.")
    return False


def scroll_to_bottom(driver):
    """Scrolls to the bottom of the page (useful for infinite scroll)."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
