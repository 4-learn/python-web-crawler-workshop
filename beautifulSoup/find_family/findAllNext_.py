from bs4 import BeautifulSoup

# 該 element 之後的所有批配 element

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, "html.parser")

# 1-1. 提取第一個匹配元素
obj_p1 = soup.find(id="p1")

# 1-2. 獲取該 element 之後的所有批配 ( 所以 p1 不算 )
obj_2 = obj_p1.findAllNext("p")
print(obj_2)

# output
"""
[<p id="c1">1</p>, <p id="c2">3</p>, <p align="blah" id="p2">This is paragraph 
      <p id="c5">5</p>.
      <b>6</b>.
      <p id="c6">7</p>.
      <b>8</b>.
    </p>, <p id="c5">5</p>, <p id="c6">7</p>]
"""
