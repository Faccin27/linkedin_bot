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

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LinkedInAutomation:
    def __init__(self, config: LinkedInConfig):
        self.config = config
        self.driver = self._setup_driver()
        self.wait = WebDriverWait(self.driver, config.timeout)

    def login(self) -> bool:
        try:
            self.driver.get("https://www.linkedin.com/login")
            self.wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(self.config.email)
            self.wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(self.config.password)
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            logger.info("Login realizado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro no login: {e}")
            return False
