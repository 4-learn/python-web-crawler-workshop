"""13 參考實作：依 SPEC.md 完成（示範 AI 應該產出的樣子）。"""
import datetime as dt
import hashlib
import json
import os
import time
import urllib.robotparser
from urllib.parse import urljoin

import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
UA = "course-crawler/1.0 (teacher)"
PCODE = "N0060001"
session = requests.Session()
session.headers["User-Agent"] = UA
_last = 0.0


def fetch(url: str) -> requests.Response:
    global _last
    if not robots.can_fetch(UA, url):
        raise RuntimeError(f"robots.txt 不允許：{url}")
    for attempt in range(4):
        time.sleep(max(0.0, 1.0 - (time.monotonic() - _last)))
        _last = time.monotonic()
        r = session.get(url, timeout=10)
        if r.status_code == 429 and attempt < 3:
            time.sleep(float(r.headers.get("Retry-After", 2 ** attempt)))
            continue
        r.raise_for_status()
        return r
    raise RuntimeError("unreachable")


robots = urllib.robotparser.RobotFileParser()
robots.parse(session.get(urljoin(BASE, "robots.txt"), timeout=10).text.splitlines())

rows, url = [], urljoin(BASE, f"v1/api/laws/{PCODE}/page-1.json")
while url:
    data = fetch(url).json()
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    for a in data["articles"]:
        rows.append({
            "pcode": PCODE, "law_name": data["name"], "slug": a["slug"], "article_no": a["article_no"],
            "chapter": a["chapter"], "content": a["content"],
            "source_url": urljoin(BASE, f"v1/laws/{PCODE}/articles/{a['slug']}.html"),
            "fetched_at": now, "content_hash": hashlib.sha256(a["content"].encode("utf-8")).hexdigest(),
        })
    url = urljoin(url, data["next"]) if data["next"] else None

assert len(rows) == data["total"]
assert len({r["slug"] for r in rows}) == len(rows)
assert rows[0]["content"].startswith("為防止職業災害")
with open("osh.jsonl", "w", encoding="utf-8") as f:
    f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
print(len(rows), "條；", rows[0]["article_no"], "～", rows[-1]["article_no"])
