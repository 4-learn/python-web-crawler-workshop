"""05 Workshop 解答：爬完勞動基準法 → labor_standards.jsonl，並與 API 逐條比對。"""
import json
import os
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
PCODE = "N0030001"
session = requests.Session()
session.headers["User-Agent"] = "course-crawler/1.0 (teacher)"


def soup_of(url):
    r = session.get(url, timeout=10)
    r.raise_for_status()
    r.encoding = "utf-8"
    return BeautifulSoup(r.text, "html.parser")


rows, url = [], BASE + f"v1/laws/{PCODE}/"
while url:
    soup = soup_of(url)
    name = soup.select_one("h1.law-title").get_text(strip=True)
    for el in soup.select("article.article"):
        link = el.select_one(".article-no a")
        rows.append({
            "pcode": PCODE, "law_name": name, "slug": el["data-slug"],
            "article_no": link.get_text(strip=True),
            "chapter": el.select_one(".chapter").get_text(strip=True),
            "content": "\n".join(p.get_text() for p in el.select(".article-content p")),
            "source_url": urljoin(url, link["href"]),
        })
    nxt = soup.select_one("a.next")
    url = urljoin(url, nxt["href"]) if nxt else None
    time.sleep(1)

with open("labor_standards.jsonl", "w", encoding="utf-8") as f:
    f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
print("HTML：", len(rows), "條")

# 與 API 逐條比對
api, url = [], BASE + f"v1/api/laws/{PCODE}/page-1.json"
while url:
    data = session.get(url, timeout=10).json()
    api += data["articles"]
    url = urljoin(url, data["next"]) if data["next"] else None
diff = [a["article_no"] for a, r in zip(api, rows) if (a["slug"], a["content"]) != (r["slug"], r["content"])]
print("API：", len(api), "條；內容不同：", diff or "無")
assert len(rows) == len(api) == 98 and not diff
