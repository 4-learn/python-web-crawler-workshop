from bs4 import BeautifulSoup

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, 'html.parser')

# 打印出 soup 對象中 <title> 標籤
print(soup.title)

fileInput.close()
