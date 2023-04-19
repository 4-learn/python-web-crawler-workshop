from bs4 import BeautifulSoup

# 第一個兒子

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, "html.parser")

# 1-1. 提取第一個匹配元素
obj_1 = soup.find(id="p2")

# 1-2. 抓出第一個兒子
list_2 = obj_1.findChild("p")
print(list_2.get("id"))

# output
"""
c5
"""
