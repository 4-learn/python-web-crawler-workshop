from bs4 import BeautifulSoup

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, 'html.parser')

# 查找符合指定 href 屬性的 <a> 標籤
result = soup.find_all(href="http://example.com/elsie")
print(result)

fileInput.close()

