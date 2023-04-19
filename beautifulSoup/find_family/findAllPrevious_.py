from bs4 import BeautifulSoup

# 上層所有批配的 element

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, "html.parser")

# 1-1. 提取第一個匹配元素
obj_1 = soup.find(id="p2")

# 1-2. 上層所有批配的 element (所以 p2 不算)
list_2 = obj_1.findAllPrevious("p")
print(list_2)

# output
"""
[<p id="c2">3</p>, <p id="c1">1</p>, <p align="center" id="p1">This is paragraph 
      <p id="c1">1</p>.
      <b>2</b>.
      <p id="c2">3</p>.
      <b>4</b>.
    </p>]
"""
