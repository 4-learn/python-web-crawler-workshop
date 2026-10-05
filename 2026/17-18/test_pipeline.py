"""pytest -q  （需先執行 collect.py 與 changes.py；DB 測試需設定 DB_USER 等環境變數）"""
import hashlib
import json
import os
import random
from urllib.parse import urljoin

import pytest
import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
FIELDS = {"pcode", "law_name", "article_no", "chapter", "content", "source_url", "fetched_at", "content_hash"}


@pytest.fixture(scope="session")
def rows():
    return [json.loads(l) for l in open("laws.jsonl", encoding="utf-8")]


@pytest.fixture(scope="session")
def index():
    return requests.get(BASE + "v1/api/laws.json", timeout=10).json()


def test_total_matches_site(rows, index):
    assert len(rows) == sum(l["article_count"] for l in index["laws"]) == 749


def test_per_law_counts(rows, index):
    for law in index["laws"]:
        assert sum(r["pcode"] == law["pcode"] for r in rows) == law["article_count"], law["pcode"]


def test_fields_and_hash(rows):
    for r in rows:
        assert FIELDS <= r.keys()
        assert r["content"] and r["content_hash"] == hashlib.sha256(r["content"].encode()).hexdigest()


def test_no_duplicates(rows):
    keys = [(r["pcode"], r["slug"]) for r in rows]
    assert len(keys) == len(set(keys))


def test_no_admin_urls(rows):
    assert not [r for r in rows if "/admin/" in r["source_url"]]


def test_sample_against_detail_pages(rows):
    """抽 3 條，打開 source_url 的詳細頁，比對 JSON-LD 的 text。"""
    from bs4 import BeautifulSoup
    for r in random.Random(42).sample(rows, 3):
        html = requests.get(r["source_url"], timeout=10)
        html.encoding = "utf-8"
        ld = json.loads(BeautifulSoup(html.text, "html.parser").select_one('script[type="application/ld+json"]').string)
        assert ld["legislationIdentifier"] == f"{r['pcode']}#{r['slug']}"
        assert ld["text"] == r["content"]


def test_changes_report():
    from changes import diff
    old = [json.loads(l) for l in open("laws.jsonl", encoding="utf-8")]
    new = [json.loads(l) for l in open("laws.v2.jsonl", encoding="utf-8")]
    added, deleted, modified, *_ = diff(old, new)
    assert (len(modified), len(deleted), len(added)) == (4, 1, 1)
    assert ("N0030001", "86-1") in added and ("N0020012", "21") in deleted
    assert "修改 | 4" in open("changes.md", encoding="utf-8").read()


@pytest.mark.skipif(not os.environ.get("DB_USER"), reason="未設定資料庫")
def test_db_idempotent():
    from load_db import load
    first = load("laws.jsonl")
    assert load("laws.jsonl") == first
