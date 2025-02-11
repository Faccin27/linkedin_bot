import os
import logging
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@dataclass
class LinkedInConfig:
    email: str
    password: str
    search_term: str
    max_connections_per_page: int = 9
    timeout: int = 10
    max_pages: int = 100

class LinkedInAutomation:
    def __init__(self, config: LinkedInConfig):
        self.config = config
        self.driver = self._setup_driver()

    def _setup_driver(self) -> webdriver.Chrome:
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        return webdriver.Chrome(options=chrome_options)

    def close(self):
        self.driver.quit()

def main():
    config = LinkedInConfig(
        email=os.getenv("LINKEDIN_EMAIL"),
        password=os.getenv("LINKEDIN_PASSWORD"),
        search_term="full stack"
    )
    bot = LinkedInAutomation(config)
    bot.close()

if __name__ == "__main__":
    main()
