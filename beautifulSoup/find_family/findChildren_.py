from bs4 import BeautifulSoup

# 找出所有批配的子 element

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, "html.parser")

# 1-1. 提取第一個匹配元素
obj_1 = soup.find(id="p2")

# 1-2. 找出所有批配的子 element
list_2 = obj_1.findChildren("p")
print(list_2)

# output
"""
[<p id="c5">5</p>, <p id="c6">7</p>]
"""
