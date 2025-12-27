from bs4 import BeautifulSoup

with open("sample_string.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# 防呆（教學用）
from bs4 import BeautifulSoup as _BS
assert isinstance(soup, _BS)

# 1️⃣ 使用文字作為最後的定位起點（anchor）
label_p = soup.find("p", string="台灣時間：")

# 2️⃣ 往上取得共同容器
label_div = label_p.parent
container = label_div.parent

# 3️⃣ 從 label_div 往前找到內容區塊
content_div = label_div.previous_sibling
while content_div and content_div.name != "div":
    content_div = content_div.previous_sibling

# 4️⃣ 往下取得時間值
time_div = content_div.find("div")
time_p = time_div.find("p")

# 5️⃣ 輸出
print(label_p.text)
print(time_p.text)
