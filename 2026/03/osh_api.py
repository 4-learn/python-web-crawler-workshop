"""03 Workshop 解答：用 API 取得職業安全衛生法全部條文，確認 61 條。"""
import os
from urllib.parse import urljoin

import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
session = requests.Session()
session.headers["User-Agent"] = "course-crawler/1.0 (teacher)"

laws = session.get(BASE + "v1/api/laws.json", timeout=10).json()["laws"]
pcode = next(l["pcode"] for l in laws if l["name"] == "職業安全衛生法")

url = BASE + f"v1/api/laws/{pcode}/page-1.json"
articles = []
while url:
    r = session.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    articles += data["articles"]
    url = urljoin(url, data["next"]) if data["next"] else None

print(pcode, data["name"], len(articles), "條")
print("第一條：", articles[0]["article_no"], articles[0]["content"][:20])
print("最後一條：", articles[-1]["article_no"])
assert len(articles) == data["total"] == 61
