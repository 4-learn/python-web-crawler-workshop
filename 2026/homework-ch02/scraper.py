"""Ch02（改版）：從爬蟲練習站取得「營造安全衛生設施標準」→ laws.json

輸出欄位沿用舊版（chapter、article_number、article_link、content），
新增 source_url、content_hash，讓 Ch03 之後照常使用。
"""
import hashlib
import json
import os
import time
import urllib.robotparser
from urllib.parse import urljoin

import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
PCODE = "N0060014"
UA = "course-crawler/1.0 (ch02-homework)"


def build_session():
    s = requests.Session()
    s.headers["User-Agent"] = UA
    r = s.get(urljoin(BASE, "robots.txt"), timeout=10)
    r.raise_for_status()
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(r.text.splitlines())
    return s, rp, float(rp.crawl_delay(UA) or 1)


def get_json(s, rp, delay, url):
    if not rp.can_fetch(UA, url):
        raise RuntimeError(f"robots.txt 不允許：{url}")
    for attempt in range(4):
        time.sleep(delay)
        r = s.get(url, timeout=10)
        if r.status_code == 429:
            time.sleep(float(r.headers.get("Retry-After", 2 ** attempt)))
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError(f"重試後仍失敗：{url}")


def to_record(a: dict) -> dict:
    chapter = " ".join(x for x in (a.get("chapter", ""), a.get("section", "")) if x)
    return {
        "chapter": chapter,
        "article_number": a["article_no"],
        "article_link": a["article_no"],
        "content": a["content"],
        "source_url": urljoin(BASE, f"v1/laws/{PCODE}/articles/{a['slug']}.html"),
        "content_hash": hashlib.sha256(a["content"].encode("utf-8")).hexdigest(),
    }


def scrape() -> list[dict]:
    s, rp, delay = build_session()
    url, laws, total = urljoin(BASE, f"v1/api/laws/{PCODE}/page-1.json"), [], None
    while url:
        d = get_json(s, rp, delay, url)
        total = d["total"]
        laws += [to_record(a) for a in d["articles"]]
        print(f"第 {d['page']}/{d['total_pages']} 頁，累計 {len(laws)} 條")
        url = urljoin(url, d["next"]) if d["next"] else None
    if len(laws) != total:
        raise SystemExit(f"筆數不符：取得 {len(laws)}，網站 {total}")
    return laws


if __name__ == "__main__":
    laws = scrape()
    with open("laws.json", "w", encoding="utf-8") as f:
        json.dump(laws, f, ensure_ascii=False, indent=2)
    print(f"已儲存 laws.json，共 {len(laws)} 條")
