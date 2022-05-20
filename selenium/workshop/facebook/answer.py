from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import time

# Login with Selenium
FACEBOOK_ID = "yillkid@gmail.com"
FACEBOOK_PW = ""
TARGET_URL = "https://www.facebook.com/groups/pythontw"

options = webdriver.ChromeOptions()
options.add_argument("incognito")
options.add_argument("headless")

driver = webdriver.Chrome(options = options)
driver.get("https://www.facebook.com")

# Get e-mail and password DOM
email =  driver.find_element_by_id("email")
password = driver.find_element_by_id("pass")

email.send_keys(FACEBOOK_ID)
password.send_keys(FACEBOOK_PW)
password.submit()

time.sleep(3)

# Goto website
driver.get(TARGET_URL)

time.sleep(3)

# Score
for x in range(1, 4):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)

# Get source
soup = BeautifulSoup(driver.page_source, 'html.parser')
titles = soup.findAll("div", {"class": "kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q"})

print("一共:" + str(len(titles)) + " 則文章...")

for title in titles:
    # print(title)
    posts = title.findAll('div', {'dir': 'auto'})
 
    for post in posts:
        if post:
            print(post.getText())

    print("----------------------------------------")

# Exit
driver.quit()
