import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from dotenv import load_dotenv

# Carregar credenciais do .env
load_dotenv()
linkedin_email = os.getenv("LINKEDIN_EMAIL")
linkedin_password = os.getenv("LINKEDIN_PASSWORD")

# Inicializar WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

# Acessar LinkedIn
driver.get("https://www.linkedin.com")
sleep(5)

# Clicar para abrir a tela de login
email = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/div/a')
email.click()
sleep(2)

# Preencher email e senha
putEmail = driver.find_element(By.XPATH, '//*[@id="username"]')
putEmail.send_keys(linkedin_email)
password = driver.find_element(By.XPATH, '//*[@id="password"]')
password.send_keys(linkedin_password)
sleep(5)

# Realizar pesquisa
pesquisar = driver.find_element(By.XPATH, '//*[@id="global-nav-typeahead"]/input')
pesquisar.click()
pesquisar.send_keys("full stack")
pesquisar.send_keys(Keys.ENTER)

# Aguardar e aplicar filtro "Pessoas"
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, '//button[@aria-pressed="false"]')))
buttons = driver.find_elements(By.XPATH, '//button[@aria-pressed="false"]')
for btn in buttons:
    if btn.text == "Pessoas":
        btn.click()
        sleep(5)

# Rolar e conectar automaticamente
i = 1
while True:
    try:
        if i >= 10:
            i = 1
            driver.execute_script("window.scroll(0, 9999)")
            avancar = driver.find_element(By.XPATH, '//*[@aria-label="Avançar"]')
            avancar.click()

        conectar = driver.find_elements(By.XPATH, '//button[contains(text(), "Conectar")]')
        for conect in conectar:
            i += 1
            conect.click()
            sleep(1)

    except:
        print("[ERRO]")
        break

try:
    driver.quit()
except Exception as e:
    print(f"Erro ao fechar o navegador: {e}")