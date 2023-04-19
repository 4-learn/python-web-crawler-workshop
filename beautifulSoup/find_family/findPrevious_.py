from bs4 import BeautifulSoup

# 上層第一個批配 element

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, "html.parser")

# 1-1. 提取第一個匹配元素
obj_1 = soup.find(id="c5")

# 1-2. 上層第一個批配 element
obj_2 = obj_1.findPrevious("p")
print(obj_2.get("id"))

# output
"""
p2
"""
