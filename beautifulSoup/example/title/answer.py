from bs4 import BeautifulSoup

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, 'html.parser')

result = soup.find_all("a")
for obj in result:
    print(obj.get("id"))

fileInput.close()
