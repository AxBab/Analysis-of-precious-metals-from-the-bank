from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Ожидание загрузки элементов (важно для динамических страниц)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import URL

def extract() -> dict:
    # Настройка опций Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Режим без графического интерфейса
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Инициализация драйвера
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    # Открытие страницы ВТБ
    driver.get(URL)

    # Ожидание загрузки курсов валют
    wait = WebDriverWait(driver, 10)
    metals_block = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "metal-rates-tablestyles__MetalRatesContainer-metal-rates-table__sc-1rb8ce4-0")))
    
    # Извлечение данных
    metals = metals_block.find_elements(By.CLASS_NAME, "service-packages-tablestyles__Row-metal-rates-table__sc-p7ct8d-0")


    # Преобразование данных в вид (Купить : цена, Продать : цена)
    gold = metals[0].text.split()
    gold = {"Продать" : "".join([gold[1], gold[2]]), "Купить" : "".join([gold[5], gold[6]])}

    silver = metals[2].text.split()
    silver = {"Продать" : silver[1], "Купить" : silver[4]}

    platinum = metals[4].text.split()
    platinum = {"Продать" : "".join([platinum[1], platinum[2]]), "Купить" : "".join([platinum[5], platinum[6]])}

    palladium = metals[6].text.split()
    palladium = {"Продать" : "".join([palladium[1], palladium[2]]), "Купить" : "".join([palladium[5], palladium[6]])}


    metals_dict = {"gold": gold, "silver": silver, "platinum": platinum, "palladium": palladium}

    driver.quit()

    return metals_dict
            
    