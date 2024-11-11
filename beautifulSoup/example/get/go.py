from bs4 import BeautifulSoup

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, 'html.parser')

# 使用 find_all 找到所有 <a> 標籤
result = soup.find_all("a")
print(type(result))  # 顯示 result 的類型

# 遍歷每個 <a> 標籤並提取其 id 屬性
for obj in result:
    print(obj.get("href"))

fileInput.close()
