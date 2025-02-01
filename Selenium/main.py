from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def search_video(name):
    opcoes = Options()
    opcoes.add_experimental_option("detach", True)
    navegador = webdriver.Chrome(options=opcoes)
    navegador.maximize_window()
    navegador.get("https://www.youtube.com")
    barrinha_de_pesquisa = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.NAME, 'search_query')))
    barrinha_de_pesquisa.send_keys(name)
    lupa = navegador.find_element(By.CLASS_NAME, "ytSearchboxComponentSearchButton")
    lupa.click()
    video = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.ID,'video-title')))
    video.click()
