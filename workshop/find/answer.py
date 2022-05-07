from bs4 import BeautifulSoup

# Open file
fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, "html.parser")

# 1. 提取第一個匹配元素
print(soup.find("p"))

# 2. 後面全部匹配兄弟節點
print(soup.find(text = "This is paragraph ").findNextSiblings("b"))

# 3. 第一個 p 的下一個 p
print(soup.find("p").findNext("p"))

# CLose file
fileInput.close()
