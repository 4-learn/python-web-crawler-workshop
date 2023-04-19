from bs4 import BeautifulSoup

# 下層第一個批配的 element

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, "html.parser")

# 1-1. 提取第一個匹配元素
obj_1 = soup.find(id="p1")

# 1-2. 下層第一個批配的 element 
obj_2 = obj_1.findNext("p")
print(obj_2.get("id"))

# output
"""
c1
"""
