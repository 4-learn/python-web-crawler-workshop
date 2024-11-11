from bs4 import BeautifulSoup

# 開啟並讀取 input.html 文件
with open("input.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, 'html.parser')

# 使用 find_all 查找所有 <a> 標籤並存入列表
a_tags = soup.find_all("a")

# 遍歷每個 <a> 標籤，提取並打印 href 屬性和文字內容
for tag in a_tags:
    print(f"{tag['href']} - {tag.text}")

# 將第一個 <a> 標籤名稱改為 <span>，再打印新標籤
a_tags[0].name = "span"
print(a_tags[0])

