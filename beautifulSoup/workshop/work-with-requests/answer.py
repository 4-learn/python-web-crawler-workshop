import requests
from bs4 import BeautifulSoup

# 發送 GET 請求並取得 HTML 內容
response = requests.get("https://travel.ettoday.net/category/%E6%A1%83%E5%9C%92/")
soup = BeautifulSoup(response.text, "html.parser")

# 找出h3標籤
list_h3 = soup.find_all("h3")

# 列印所有h3
for h3 in list_h3:
    print(h3.text.strip())
