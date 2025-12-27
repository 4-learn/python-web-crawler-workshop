from bs4 import BeautifulSoup

# 從檔案讀取 HTML
with open("input.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# 1️⃣ 使用 find_all 取得所有 <a> 標籤（ResultSet）
a_tags = soup.find_all("a")

# 2️⃣ 遍歷每個 Tag，印出 href 與文字內容
for tag in a_tags:
    print(f"{tag['href']} - {tag.text}")

# 3️⃣ 將其中一個 Tag 的標籤名稱改為 <span>
a_tags[0].name = "span"
print(a_tags[0])

