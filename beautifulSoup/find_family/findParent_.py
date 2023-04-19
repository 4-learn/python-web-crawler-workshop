from bs4 import BeautifulSoup

# 第一個父親 element

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, "html.parser")

# 1-1. 提取第一個匹配元素
obj_1 = soup.find(id="c5")

# 1-2. 第一個批配父親節點
obj_2 = obj_1.findParent("p")
print(obj_2.get("id"))

# output
"""
p2
"""
