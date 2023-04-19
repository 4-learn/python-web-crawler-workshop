from bs4 import BeautifulSoup

# 全部批配的父親 element

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, "html.parser")

# 1-1. 提取第一個匹配元素
obj_1 = soup.find(id="c5")

# 1-2. 全部批配父親節點
list_2 = obj_1.findParents("p")
print(list_2)

# output
"""
[<p align="blah" id="p2">This is paragraph 
      <p id="c5">5</p>.
      <b>6</b>.
      <p id="c6">7</p>.
      <b>8</b>.
    </p>]
"""
