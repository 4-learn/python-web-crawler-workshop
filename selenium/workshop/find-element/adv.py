from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 初始化選項
options = webdriver.ChromeOptions()
options.add_argument("incognito")  # 開啟無痕模式

# 安裝並設定 WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get("file:///home/yillkid/workspace/python-web-crawler/selenium/workshop/find-element/input.html")  # 變更為您的實際檔案位置

# 等待用戶手動輸入用戶名和密碼
print("請在瀏覽器中輸入用戶名和密碼，然後在這裡輸入 'y' 繼續。")
while True:
    user_input = input()  # 從控制台獲取輸入
    if user_input.lower() == 'y':
        break
    else:
        print("未識別的輸入，如果完成輸入，請輸入 'y'。")

# 獲取表單元素並提交
elem_form = driver.find_element(By.ID, "loginForm")
elem_form.submit()

while True:
    pass
