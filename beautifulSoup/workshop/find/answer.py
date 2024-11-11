from bs4 import BeautifulSoup

# 載入 HTML 文件
html_doc = ""
with open('input.html', 'r', encoding='utf-8') as file:
    html_doc = file.read()

# 解析 HTML 文件
soup = BeautifulSoup(html_doc, 'html.parser')

# 從 body 標籤開始
body = soup.find('body')

# 使用 findChild 找到第一個 <div> 標籤
first_div = body.findChild('div')

# 使用 findChild 找到 <div> 的子 <div>，即第二層 <div>
second_div = first_div.findChild('div')

# 使用 findNextSibling 找到第三個 <div>，其中包含「台灣時間：」
tw_time_div = second_div.findNextSibling('div')
print(tw_time_div.text.strip())

# 使用 findPreviousSibling 找到含時間的 <div> 並取得其子 <p> 的內容
pre_div = tw_time_div.findPreviousSibling('div')
time_div = pre_div.findChild('div').findChild('p').text.strip()
print(time_div)

