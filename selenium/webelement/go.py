from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 設定 WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 開啟 HTML 文件
driver.get("file:///home/yillkid/workspace/4-learn/python-web-crawler/selenium/webelement/input.html")

# 使用 find_element 查找表單元素
result = driver.find_element(By.NAME, "continue")

# 顯示標題和元素屬性
print(driver.title)
print(result.get_attribute("value"))
