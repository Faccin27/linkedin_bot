import os
import logging
from time import sleep
from typing import List, Optional
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class LinkedInConfig:
    email: str
    password: str
    search_term: str
    max_connections_per_page: int = 9
    timeout: int = 10
    max_pages: int = 100  # Número máximo de páginas a percorrer
    base_url: str = "https://www.linkedin.com/login"

class LinkedInAutomation:
    def __init__(self, config: LinkedInConfig):
        self.config = config
        self.driver = self._setup_driver()
        self.wait = WebDriverWait(self.driver, config.timeout)
        self.total_connections = 0

    def _setup_driver(self) -> webdriver.Chrome:
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return webdriver.Chrome(options=chrome_options)

    def login(self) -> bool:
        try:
            self.driver.get(self.config.base_url)
            
            self.wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(self.config.email)
            self.wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(self.config.password)
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            
            self.wait.until(EC.presence_of_element_located((By.ID, "global-nav")))
            logger.info("Login realizado com sucesso")
            return True
            
        except TimeoutException:
            logger.error("Falha no login - timeout")
            return False
        except Exception as e:
            logger.error(f"Erro durante o login: {e}")
            return False

    def search_and_connect(self) -> None:
        try:
            # Realiza a pesquisa
            search_box = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.search-global-typeahead__input"))
            )
            search_box.clear()
            search_box.send_keys(self.config.search_term + Keys.ENTER)
            sleep(3)  # Espera os resultados carregarem

            # Seleciona a aba "Pessoas"
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-pressed='false']"))
            )
            people_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[aria-pressed='false']")
            for button in people_buttons:
                if "Pessoas" in button.text:
                    button.click()
                    sleep(3)  # Espera os resultados de pessoas carregarem
                    break

            page_number = 1
            while page_number <= self.config.max_pages:
                logger.info(f"Processando página {page_number}")
                
                # Rola a página para garantir que todos os elementos sejam carregados
                self._scroll_page()
                
                if self._process_current_page():
                    logger.info(f"Conexões enviadas na página {page_number}")
                else:
                    logger.info(f"Nenhuma conexão disponível na página {page_number}")
                
                if not self._next_page():
                    logger.info("Fim das páginas alcançado")
                    break
                    
                page_number += 1
                sleep(3)  # Espera a nova página carregar

            logger.info(f"Total de solicitações de conexão enviadas: {self.total_connections}")

        except Exception as e:
            logger.error(f"Erro durante a busca e conexão: {e}")

    def _scroll_page(self) -> None:
        """Rola a página para garantir que todos os elementos sejam carregados."""
        try:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                # Rola até o final da página
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)  # Espera o conteúdo carregar
                
                # Calcula a nova altura da página
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
        except Exception as e:
            logger.error(f"Erro ao rolar a página: {e}")

    def _process_current_page(self) -> bool:
        """Processa os perfis da página atual. Retorna True se enviou alguma conexão."""
        try:
            connect_buttons = self.driver.find_elements(
                By.CSS_SELECTOR,
                "button.artdeco-button--secondary"
            )

            connections_made = 0
            for button in connect_buttons:
                try:
                    if "Conectar" in button.text:
                        if self._send_connection_request(button):
                            connections_made += 1
                            self.total_connections += 1
                            sleep(2)  # Intervalo entre conexões
                            
                        if connections_made >= self.config.max_connections_per_page:
                            break
                except ElementClickInterceptedException:
                    continue  # Pula para o próximo botão se este não puder ser clicado

            return connections_made > 0

        except Exception as e:
            logger.error(f"Erro ao processar página: {e}")
            return False

    def _send_connection_request(self, button: webdriver.remote.webelement.WebElement) -> bool:
        """Envia uma solicitação de conexão. Retorna True se foi bem-sucedido."""
        try:
            if not button.is_displayed() or not button.is_enabled():
                return False

            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            sleep(1)
            button.click()
            sleep(1)
            
            # Procura pelo botão "Enviar" ou "Adicionar nota"
            try:
                send_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.artdeco-button--primary")
                for send_button in send_buttons:
                    if "Enviar" in send_button.text:
                        send_button.click()
                        logger.info("Solicitação de conexão enviada com sucesso")
                        return True
            except:
                logger.info("Não foi possível encontrar o botão de enviar")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao enviar solicitação de conexão: {e}")
            return False

    def _next_page(self) -> bool:
        """Navega para a próxima página de resultados."""
        try:
            next_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Avançar']")
            for button in next_buttons:
                if button.is_enabled() and button.is_displayed():
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    sleep(1)
                    button.click()
                    sleep(3)  # Espera a nova página carregar
                    return True
            return False
        except Exception as e:
            logger.error(f"Erro ao navegar para próxima página: {e}")
            return False

    def close(self) -> None:
        try:
            self.driver.quit()
            logger.info("Navegador fechado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao fechar o navegador: {e}")

def main():
    load_dotenv()
    
    config = LinkedInConfig(
        email=os.getenv("LINKEDIN_EMAIL"),
        password=os.getenv("LINKEDIN_PASSWORD"),
        search_term="full stack",
        max_connections_per_page=9,
        max_pages=100
    )
    
    automation = LinkedInAutomation(config)
    
    try:
        if automation.login():
            automation.search_and_connect()
    finally:
        automation.close()

if __name__ == "__main__":
    main()


# recode complete