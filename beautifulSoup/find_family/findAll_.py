from bs4 import BeautifulSoup

# 所有批配的兒子

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, "html.parser")

# 1-1. 所有批配的兒子
list_1 = soup.findAll("p")
print(list_1)

# output
"""
[<p align="center" id="p1">This is paragraph 
      <p id="c1">1</p>.
      <b>2</b>.
      <p id="c2">3</p>.
      <b>4</b>.
    </p>, <p id="c1">1</p>, <p id="c2">3</p>, <p align="blah" id="p2">This is paragraph 
      <p id="c5">5</p>.
      <b>6</b>.
      <p id="c6">7</p>.
      <b>8</b>.
    </p>, <p id="c5">5</p>, <p id="c6">7</p>]
"""
