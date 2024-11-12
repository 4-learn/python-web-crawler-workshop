from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 初始化 WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 開啟 Yahoo 首頁
driver.get("https://tw.yahoo.com")

# 等待頁面載入
time.sleep(3)

# 使用 find_element 查找頁面中的第一個 <a> 標籤
link_element = driver.find_element(By.TAG_NAME, "a")

# 打印 WebElement 物件
print("找到的 WebElement:", link_element)

# 關閉瀏覽器
driver.quit()
