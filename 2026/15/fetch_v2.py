"""15 Workshop 解答 1/2：v1 爬蟲在 v2 壞掉的地方，與修正後的 v2 版。

v1 → v2 差異：
- 列表 API：v1/api/laws.json {laws:[pcode,name,...]} → v2/api/laws.json {items:[code,title,updated,articles]}
- 條文 API：v1/api/laws/{pcode}/page-N.json {articles, next} → v2/api/laws/{code}/N.json {items, pages}，無 next
- 條文欄位：slug/article_no/content → id/number/text
- HTML：article.article → tr.row[data-article]；分頁網址 page-N.html → p/N.html；每頁 20 → 25 條
"""
import hashlib
import json
import os
import time

import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
session = requests.Session()
session.headers["User-Agent"] = "course-crawler/1.0 (teacher)"


def get(url):
    time.sleep(0.3)
    r = session.get(url, timeout=10)
    r.raise_for_status()
    return r.json()


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def crawl_v1():
    from urllib.parse import urljoin
    out = []
    for law in get(BASE + "v1/api/laws.json")["laws"]:
        url = BASE + f"v1/api/laws/{law['pcode']}/page-1.json"
        while url:
            d = get(url)
            out += [{"pcode": law["pcode"], "slug": a["slug"], "article_no": a["article_no"],
                     "content": a["content"], "content_hash": sha(a["content"])} for a in d["articles"]]
            url = urljoin(url, d["next"]) if d["next"] else None
    return out


def crawl_v2():
    out = []
    laws = get(BASE + "v2/api/laws.json")["items"]
    for law in laws:
        page = 1
        while True:
            d = get(BASE + f"v2/api/laws/{law['code']}/{page}.json")
            out += [{"pcode": law["code"], "slug": a["id"], "article_no": a["number"],
                     "content": a["text"], "content_hash": sha(a["text"])} for a in d["items"]]
            if page >= d["pages"]:
                break
            page += 1
        got = sum(1 for r in out if r["pcode"] == law["code"])
        assert got == law["articles"], (law["code"], got, law["articles"])  # 筆數守門
    if not out:
        raise SystemExit("v2 抓到 0 筆：選擇器或 API 格式又變了")
    return out


if __name__ == "__main__":
    for name, fn in [("v1", crawl_v1), ("v2", crawl_v2)]:
        rows = fn()
        with open(f"{name}.jsonl", "w", encoding="utf-8") as f:
            f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
        print(name, len(rows), "條")
