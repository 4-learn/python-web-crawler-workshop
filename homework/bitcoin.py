from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def get_bitcoin_price():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.headless = True  # 無頭模式
    driver = webdriver.Chrome(service=service, options=options)

    driver.get('https://www.coindesk.com/coindesk20')  # 示例網址，請替換為實際網址
    price_element = driver.find_element(By.XPATH, '//*[@id="the-price"]')  # 使用適合的 XPATH
    price = price_element.text
    driver.quit()
    return price
