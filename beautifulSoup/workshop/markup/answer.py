from bs4 import BeautifulSoup

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, 'html.parser')

print(soup.prettify())
fileInput.close()
