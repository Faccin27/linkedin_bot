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

from selenium.common.exceptions import TimeoutException

def login(self) -> bool:
    try:
        self.driver.get("https://www.linkedin.com/login")
        self.wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(self.config.email)
        self.wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(self.config.password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.wait.until(EC.presence_of_element_located((By.ID, "global-nav")))
        logger.info("Login realizado com sucesso")
        return True
    except TimeoutException:
        logger.error("Falha no login - timeout")
        return False

def search_and_connect(self):
    try:
        search_box = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.search-global-typeahead__input"))
        )
        search_box.clear()
        search_box.send_keys(self.config.search_term + Keys.ENTER)
        sleep(3)
    except Exception as e:
        logger.error(f"Erro ao buscar conexões: {e}")

def _scroll_page(self):
    try:
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    except Exception as e:
        logger.error(f"Erro ao rolar a página: {e}")

def _send_connection_request(self, button):
    try:
        button.click()
        sleep(1)
        send_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.artdeco-button--primary")
        for send_button in send_buttons:
            if "Enviar" in send_button.text:
                send_button.click()
                logger.info("Solicitação de conexão enviada com sucesso")
                return True
    except Exception as e:
        logger.error(f"Erro ao enviar solicitação de conexão: {e}")
    return False

def close(self):
    try:
        self.driver.quit()
        logger.info("Navegador fechado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao fechar o navegador: {e}")

def main():
    config = LinkedInConfig(
        email=os.getenv("LINKEDIN_EMAIL"),
        password=os.getenv("LINKEDIN_PASSWORD"),
        search_term="full stack"
    )
    automation = LinkedInAutomation(config)
    
    try:
        if automation.login():
            automation.search_and_connect()
    finally:
        automation.close()

if __name__ == "__main__":
    main()
