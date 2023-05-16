from bs4 import BeautifulSoup

# Open file
fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, "html.parser")

# 1. 第一個 node
a = soup.find("p")
print(type(a))

# 2. 後面全部匹配兄弟節
b = soup.find(text = "This is paragraph ")
print(type(b))

# CLose file
fileInput.close()

"""
output:
<class 'bs4.element.Tag'>
<class 'bs4.element.NavigableString'>

b 為 bs4.element.NavigableString，也就是 b 的角色為 string
因此 findNextSiblings 指的是 "This is paragraph " 之後的所有兄弟 node
為：[<b>one</b>]
"""
