from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 設定 WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 開啟 HTML 文件
driver.get("file:///home/yillkid/workspace/4-learn/python-web-crawler/selenium/workshop/webelement/input.html")

# 填寫 username 和 password 欄位
username_field = driver.find_element(By.NAME, "username")
password_field = driver.find_element(By.NAME, "password")

username_field.send_keys("test_user")
password_field.send_keys("test_password")

# 提交表單
login_button = driver.find_element(By.NAME, "continue")
login_button.submit()

# 顯示成功訊息
print("表單已提交")
