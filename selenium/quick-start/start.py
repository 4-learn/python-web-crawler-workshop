from selenium import webdriver
from selenium.webdriver.chrome.options import Options

driver = webdriver.Chrome()
driver.get("https://www.google.com")

print(driver.title)  
