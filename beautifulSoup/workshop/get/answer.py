from bs4 import BeautifulSoup

# 從檔案讀取 HTML
with open("input.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# 1️⃣ 使用 find_all 取得所有 <a> 標籤
a_tags = soup.find_all("a")

# 2️⃣ 遍歷每個 Tag，使用 get() 安全取得屬性
for tag in a_tags:
    href = tag.get("href")
    text = tag.text
    print(f"{href} - {text}")

