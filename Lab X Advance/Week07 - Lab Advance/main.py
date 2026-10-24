# agentic-web-scraper/main.py
import os
import logging

from src.config_parser import ConfigParser
from src.scraper_agent import ScraperAgent

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    """Main entry point: load config -> run the scraping agent."""
    os.chdir(BASE_DIR)  # ให้ไฟล์ผลลัพธ์ไปอยู่ที่ data/ เสมอ ไม่ว่าจะรันจากโฟลเดอร์ไหน
    config_file_path = os.path.join(BASE_DIR, 'configs', 'example_site_config.json')
    try:
        config = ConfigParser(config_file_path).load_config()
        # headless=False ถ้าอยากเห็นเบราว์เซอร์ทำงานจริง
        agent = ScraperAgent(config, browser='chrome', headless=True)
        agent.run()
    except FileNotFoundError as e:
        logging.error(f"Configuration file error: {e}")
    except ValueError as e:
        logging.error(f"Configuration validation error: {e}")
    except Exception as e:
        logging.critical(f"An unexpected error occurred during execution: {e}")


if __name__ == "__main__":
    main()
