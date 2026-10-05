"""14 Workshop 解答：替第 13 節的爬蟲寫測試。

pytest -q test_osh.py --jsonl ../13/osh.jsonl
"""
import hashlib
import json
import os
import random
from urllib.parse import urljoin

import pytest
import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")


@pytest.fixture(scope="session")
def rows(request):
    with open(request.config.getoption("--jsonl"), encoding="utf-8") as f:
        return [json.loads(line) for line in f]


@pytest.fixture(scope="session")
def source():
    out, url = [], BASE + "v1/api/laws/N0060001/page-1.json"
    while url:
        d = requests.get(url, timeout=10).json()
        out += d["articles"]
        url = urljoin(url, d["next"]) if d["next"] else None
    return out


def test_count(rows, source):
    """筆數對照：與來源的總數相同（抓得到「漏最後一頁」）。"""
    assert len(rows) == len(source)


def test_unique_and_complete(rows, source):
    """沒有重複、沒有缺號。"""
    slugs = [r["slug"] for r in rows]
    assert len(slugs) == len(set(slugs))
    assert set(slugs) == {a["slug"] for a in source}


def test_sample_content(rows, source):
    """隨機抽 5 條比對原文（抓得到「欄位錯位」）。"""
    truth = {a["slug"]: a for a in source}
    for r in random.sample(rows, 5):
        assert r["content"] == truth[r["slug"]]["content"]
        assert r["article_no"] == truth[r["slug"]]["article_no"]


def test_hash_and_url(rows):
    for r in rows:
        assert r["content_hash"] == hashlib.sha256(r["content"].encode("utf-8")).hexdigest()
        assert "/admin/" not in r["source_url"]
        assert r["source_url"].endswith(f"/v1/laws/{r['pcode']}/articles/{r['slug']}.html")
