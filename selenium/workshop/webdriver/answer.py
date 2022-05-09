from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.add_argument("incognito")

driver = webdriver.Chrome(options = options)
driver.get("https://www.google.com")

print(driver.title)
