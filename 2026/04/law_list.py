"""04 Workshop 解答：從法規列表取出 9 部法規的名稱、pcode、條文數。"""
import csv
import os
import sys

import requests
from bs4 import BeautifulSoup

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
r = requests.get(BASE + "v1/laws/", headers={"User-Agent": "course-crawler/1.0 (teacher)"}, timeout=10)
r.raise_for_status()
r.encoding = "utf-8"
soup = BeautifulSoup(r.text, "html.parser")

rows = [
    {
        "name": tr.select_one("td.law-name a").get_text(strip=True),
        "pcode": tr["data-pcode"],
        "count": int(tr.select_one("td.count").get_text()),
    }
    for tr in soup.select("table.law-list tr.law")
]
writer = csv.DictWriter(sys.stdout, fieldnames=["name", "pcode", "count"])
writer.writeheader()
writer.writerows(rows)
print("合計", len(rows), "部、", sum(r["count"] for r in rows), "條", file=sys.stderr)
assert len(rows) == int(soup.select_one("#law-count").get_text()) == 9
