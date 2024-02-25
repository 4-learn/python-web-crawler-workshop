from bs4 import BeautifulSoup
html_doc = ""
with open('input.html', 'r', encoding='utf-8') as file:
    html_doc = file.read()

soup = BeautifulSoup(html_doc, 'html.parser')

# 從 body 標籤開始
body = soup.find('body')

# 使用 findChild 找到第一個 div
first_div = body.findChild('div')

# 使用 findSibling 找到第二個 div
second_div = first_div.findChild('div')
tw_time_div = second_div.findNextSibling('div')
print(tw_time_div.text)

# 回頭
pre_div = tw_time_div.findPreviousSibling('div')
time_div = pre_div.findChild('div').findChild('p').text
print(time_div)
