from bs4 import BeautifulSoup

# 第一個批配的兒子

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, "html.parser")

# 1-1. 提取第一個匹配元素
obj_1 = soup.find("p")
print(obj_1.get("id"))

# 1-2. 提取第一個匹配元素
obj_2 = obj_1.find("p")
print(obj_2.get("id"))

# output
"""
p1
c1
"""
