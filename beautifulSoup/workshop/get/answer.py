from bs4 import BeautifulSoup

fileInput = open("input.html", "r")
soup = BeautifulSoup(fileInput, 'html.parser')

listResult = soup.find_all("a")
for obj in listResult:
    if (obj.get("class") == ["sister"] and obj.get("id") == "link1"):
        print(obj.text)

fileInput.close()
