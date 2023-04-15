import requests
from bs4 import BeautifulSoup
from db import *

# 資料庫
create_db()
create_table()

# 網站
URL_SITE = "https://travel.ettoday.net/category/%E5%8F%B0%E5%8C%97/"

response = requests.get(URL_SITE)
soup = BeautifulSoup(response.text, "html.parser")

# 內文
SetObjs = soup.find_all("div", class_ = "box_0 clearfix")

# 爬取標題 / 內文
list_title = None
list_content = None
for obj in SetObjs:
    # 尋找所有 h3 tag
    list_title = obj.findChildren("h3")
    # 尋找所有 p tag
    list_content = obj.findChildren("p", recursive = False)

    for index in range(0, len(list_title)):
        # print(list_title[0].text)
        # print(list_content[0].text)

        # 插入資料庫
        insert_data(list_title[0].text, list_content[0].text)

# 顯示
show_data()
