from bs4 import BeautifulSoup

# 1️⃣ 讀取 HTML 檔案
with open("input.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# 防呆（教學用，建議保留）
from bs4 import BeautifulSoup as _BS
assert isinstance(soup, _BS)

# 2️⃣ 使用 attribute 作為穩定起點（anchor）
container = soup.find("div", id="container")

# 3️⃣ 找到「時間數字」區塊
#    先定位 data-role="time"，再往下找 p
time_div = container.find("div", attrs={"data-role": "time"})
time_p = time_div.find("p")

# 4️⃣ 找到「台灣時間：」
#    先定位 class="label"，再往下找 p
label_div = container.find("div", class_="label")
label_p = label_div.find("p")

# 5️⃣ 輸出結果
print(label_p.text)
print(time_p.text)
