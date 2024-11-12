from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 設定 WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 開啟 HTML 文件
driver.get("https://udn.com/news/index")

# 查找所有 <p> 標籤
paragraphs = driver.find_elements(By.TAG_NAME, "p")

# 列印每個 <p> 標籤的文字
for paragraph in paragraphs:
    print(paragraph.text)

# 關閉瀏覽器
driver.quit()
