from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 設置 Chrome 瀏覽器為無痕模式
options = webdriver.ChromeOptions()
options.add_argument("--incognito")

# 初始化 WebDriver 並應用無痕模式
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 開啟 Google 網站
driver.get("https://www.google.com")

# 顯示頁面標題
print(driver.title)
