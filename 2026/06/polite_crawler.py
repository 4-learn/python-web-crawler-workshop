"""06 Workshop 解答：先觸發 429，再修成有禮貌的版本。請對教室版 server.py 執行。

PLAYGROUND=http://老師IP:8000/ python polite_crawler.py
"""
import os
import time
import urllib.robotparser
from urllib.parse import urljoin

import requests

BASE = os.environ.get("PLAYGROUND", "http://127.0.0.1:8000/")
UA = "course-crawler/1.0 (teacher)"
pages = [f"v1/api/laws/N0030001/page-{n}.json" for n in range(1, 6)] + ["v1/admin/"]

print("=== 1. 沒禮貌：不等待、不看 robots.txt ===")
codes = [requests.get(BASE + pages[0], timeout=5).status_code for _ in range(30)]
print({c: codes.count(c) for c in sorted(set(codes))}, "← 出現 429")
time.sleep(5)  # 讓伺服器的額度回復

print("=== 2. 有禮貌 ===")
session = requests.Session()
session.headers["User-Agent"] = UA
r = session.get(urljoin(BASE, "robots.txt"), timeout=10)
rp = urllib.robotparser.RobotFileParser()
rp.parse(r.text.splitlines())
delay = float(rp.crawl_delay(UA) or 1)

for path in pages:
    url = BASE + path
    if not rp.can_fetch(UA, url):
        print("robots.txt 禁止，跳過", path)
        continue
    for attempt in range(4):
        r = session.get(url, timeout=10)
        if r.status_code != 429:
            break
        wait = float(r.headers.get("Retry-After", 2 ** attempt))
        print("429，等", wait, "秒")
        time.sleep(wait)
    print(r.status_code, path)
    time.sleep(delay)
