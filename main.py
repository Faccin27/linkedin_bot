import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
linkedin_email = os.getenv("LINKEDIN_EMAIL")
linkedin_password = os.getenv("LINKEDIN_PASSWORD")

# Iniciar o WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

# Acessar o LinkedIn
driver.get("https://www.linkedin.com")
sleep(5)

# Clicar no botão de login
email = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/div/a')
email.click()
sleep(2)

# Preencher email e senha
putEmail = driver.find_element(By.XPATH, '//*[@id="username"]')
putEmail.send_keys(linkedin_email)

password = driver.find_element(By.XPATH, '//*[@id="password"]')
password.send_keys(linkedin_password)

sleep(5)

from selenium.webdriver.common.keys import Keys

# Realizar pesquisa após login
pesquisar = driver.find_element(By.XPATH, '//*[@id="global-nav-typeahead"]/input')
pesquisar.click()
pesquisar.send_keys("full stack")
pesquisar.send_keys(Keys.ENTER)

sleep(5)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Aguardar carregamento da página
wait = WebDriverWait(driver, 10)
wait.until(
    EC.presence_of_element_located((By.XPATH, '//button[@aria-pressed="false"]'))
)

# Clicar no filtro "Pessoas"
buttons = driver.find_elements(By.XPATH, '//button[@aria-pressed="false"]')
for btn in buttons:
    if btn.text == "Pessoas":
        btn.click()
        sleep(5)
        
        conectar = driver.find_elements(
    By.XPATH,
    '//button[@class="artdeco-button artdeco-button--2 artdeco-button--secondary ember-view"]',
)
for conect in conectar:
    if conect.text == "Conectar":
        conect.click()
        sleep(1)
        
        i = 1
while True:
    try:
        if i >= 10:
            i = 1
            driver.execute_script("window.scroll(0, 9999)")
            avancar = driver.find_element(By.XPATH, '//*[@aria-label="Avançar"]')
            avancar.click()
        conectar = driver.find_elements(
            By.XPATH,
            '//button[@class="artdeco-button artdeco-button--2 artdeco-button--secondary ember-view"]',
        )
        for conect in conectar:
            i += 1
            if conect.text == "Conectar":
                conect.click()
                sleep(1)
    except:
        print("[ERRO]")