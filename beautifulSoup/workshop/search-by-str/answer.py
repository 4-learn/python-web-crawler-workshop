from bs4 import BeautifulSoup

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, 'html.parser')

result = soup.find_all("a", string = ["Elsie", "Lacie"])
fileInput.close()

print(result)
