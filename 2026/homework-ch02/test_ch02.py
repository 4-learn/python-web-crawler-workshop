import hashlib
import json
import os

import pytest
import requests

from regulation_store import RegulationStore

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
OLD_FIELDS = {"chapter", "article_number", "article_link", "content"}


@pytest.fixture(scope="module")
def laws():
    with open("laws.json", encoding="utf-8") as f:
        return json.load(f)


def test_count_matches_api(laws):
    total = requests.get(BASE + "v1/api/laws/N0060014/page-1.json", timeout=10).json()["total"]
    assert len(laws) == total


def test_schema_backward_compatible(laws):
    for law in laws:
        assert OLD_FIELDS <= law.keys()
        assert law["article_number"].startswith("第 ") and law["article_number"].endswith(" 條")
        assert law["content_hash"] == hashlib.sha256(law["content"].encode("utf-8")).hexdigest()


def test_no_duplicates(laws):
    nos = [l["article_number"] for l in laws]
    assert len(nos) == len(set(nos))


@pytest.mark.parametrize("etype, word", [("fall", "墜落"), ("excavation", "開挖")])
def test_keyword_match(laws, etype, word):
    law = RegulationStore(laws).match_event({"type": etype})
    assert law is not None and word in law["content"]


def test_unknown_event_returns_none(laws):
    assert RegulationStore(laws).match_event({"type": "unknown"}) is None


def test_empty_store():
    assert RegulationStore([]).match_event({"type": "fall"}) is None
