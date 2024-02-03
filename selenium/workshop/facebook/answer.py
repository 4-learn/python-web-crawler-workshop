from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


from bs4 import BeautifulSoup

import time

# Login with Selenium
FACEBOOK_ID = "yillkid@gmail.com"
FACEBOOK_PW = "自行填入"
TARGET_URL = "https://www.facebook.com/groups/pythontw"

options = webdriver.ChromeOptions()
options.add_argument("incognito")
# options.add_argument("headless")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options = options)
driver.get("https://www.facebook.com")

print("go " + driver.title )

# Get e-mail and password DOM
# email =  driver.find_element_by_id("email")
email =  driver.find_element(By.ID, "email")
password = driver.find_element(By.ID, "pass")
login = driver.find_element(By.NAME, "login")

email.send_keys(FACEBOOK_ID)
password.send_keys(FACEBOOK_PW)
login.submit()

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
titles = soup.findAll("div", {"class": "xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a"})

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
