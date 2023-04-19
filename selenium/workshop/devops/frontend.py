from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json

d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { u'browser':'ALL' }

options = webdriver.ChromeOptions()
# options.add_argument("headless")
options.add_argument("incognito")

driver = webdriver.Chrome(options = options, desired_capabilities=d)

## Signup
driver.get("https://yillkid.github.io/ntc-python-crawler-workshop-frontent/signup.html")

# Get elements
elem_email = driver.find_element(By.ID, "email")
elem_username = driver.find_element(By.ID, "username")
elem_password = driver.find_element(By.ID, "password")
elem_cfm_password = driver.find_element(By.ID, "cfm_password")

# Send Key
elem_email.send_keys("ntc-test-123@gmail.com")
elem_username.send_keys("1111111111")
elem_password.send_keys("1111111111")
elem_cfm_password.send_keys("1111111111")

# Submit
elem_btn = driver.find_element(By.TAG_NAME, "button")
elem_btn.click()

## Signin
driver.get("https://yillkid.github.io/ntc-python-crawler-workshop-frontent/signin.html")

# Get elements
elem_email = driver.find_element(By.ID, "email")
elem_password = driver.find_element(By.ID, "password")

# Send Key
elem_email.send_keys("ntc-test-123@gmail.com")
elem_password.send_keys("1111111111")

# Submit
elem_btn = driver.find_element(By.TAG_NAME, "button")
elem_btn.click()

time.sleep(1)

for entry in driver.get_log('browser'):
    if ("JWT" in entry["message"]):
        print(entry)
        with open("frontend.json", "w") as fp:
            json.dump(entry, fp)
