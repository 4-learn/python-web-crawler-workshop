from bs4 import BeautifulSoup

# 前面全部批配兄弟節點

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, "html.parser")

# 1-1. 提取第一個匹配元素
obj_1 = soup.find(id="p2")

# 1-2. 前面全部批配兄弟節點
list_2 = obj_1.findPreviousSiblings("p")
print(list_2)

# output
"""
[<p align="center" id="p1">This is paragraph 
      <p id="c1">1</p>.
      <b>2</b>.
      <p id="c2">3</p>.
      <b>4</b>.
    </p>]
"""
