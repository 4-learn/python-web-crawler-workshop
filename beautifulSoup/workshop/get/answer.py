from bs4 import BeautifulSoup

# 開啟 HTML 檔案
fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, 'html.parser')

# 找到所有 <a> 標籤
result = soup.find_all("a")

# 提取符合條件的內容
for obj in result:
    # 假設我們只輸出第一個 <a> 標籤的文字
    print(obj.text)
    break  # 只輸出第一個符合條件的 <a> 標籤

fileInput.close()
