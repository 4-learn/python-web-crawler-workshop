import requests
from bs4 import BeautifulSoup

URL_SITE = "https://travel.ettoday.net/category/%E5%8F%B0%E5%8C%97/"

response = requests.get(URL_SITE)
soup = BeautifulSoup(response.text, "html.parser")

# 內文
SetObjs = soup.find_all("div", class_ = "box_0 clearfix")

# 標題 
for obj in SetObjs:
    # 尋找所有 h3 tag
    list_child = obj.findChildren("h3")
    for obj in list_child:
        for obj2 in list_child[0]:
            print(obj2.text)

for obj in SetObjs:
    # 尋找所有 p tag
    list_child = obj.findChildren("p", recursive = False)
    
    # 過濾時間
    for obj2 in list_child[0].children:
        if obj2.name == "em":
            continue
        print(obj2.text)
