from bs4 import BeautifulSoup

with open("input.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

body = soup.find("body")
container = body.find("div")

inner = container.find("div")
time_p = inner.find("div").find("p")

label_div = inner.next_sibling
while label_div and label_div.name != "div":
    label_div = label_div.next_sibling

label_p = label_div.find("p")

print(label_p.text)
print(time_p.text)
