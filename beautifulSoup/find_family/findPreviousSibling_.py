from bs4 import BeautifulSoup

# 前面第一個批配的兄弟 element

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, "html.parser")

# 1-1. 提取第一個匹配元素
obj_1 = soup.find(id="p2")

# 1-2. 前面第一個批配的兄弟 element
obj_2 = obj_1.findPreviousSibling("p")
print(obj_2.get("id"))

# output
"""
p1
"""
