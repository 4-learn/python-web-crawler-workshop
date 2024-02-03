from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("incognito")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options = options)
driver.get("file:///home/yillkid/input.html")

# Get elements
elem_form = driver.find_element(By.ID, "loginForm")
elem_username = driver.find_element(By.NAME, "username")
elem_password = driver.find_element(By.NAME, "password")

# Send Key
elem_username.send_keys("tom")
elem_password.send_keys("22")

# Submit
elem_form.submit()
