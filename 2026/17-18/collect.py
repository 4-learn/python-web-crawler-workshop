"""步驟 1：蒐集 v1 全部法規 → laws.jsonl

工具選擇（見 README）：
- 法規清單、條文：關卡 2 的 JSON API（requests）——最快、最穩、有 total 可驗證。
- 交叉驗證：隨機選 1 部法規，用關卡 1 的 HTML（requests + bs4）逐條比對內容。
"""
import datetime as dt
import hashlib
import json
import os
import random
import sys
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from polite import PoliteSession

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
OUT = "laws.jsonl"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def from_api(s: PoliteSession) -> tuple[list[dict], dict]:
    index = s.json(BASE + "v1/api/laws.json")
    rows, expected = [], {}
    for law in index["laws"]:
        expected[law["pcode"]] = law["article_count"]
        url = BASE + f"v1/api/laws/{law['pcode']}/page-1.json"
        while url:
            d = s.json(url)
            now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
            for a in d["articles"]:
                rows.append({
                    "pcode": law["pcode"], "law_name": law["name"], "slug": a["slug"],
                    "article_no": a["article_no"], "chapter": a["chapter"], "content": a["content"],
                    "source_url": urljoin(BASE, f"v1/laws/{law['pcode']}/articles/{a['slug']}.html"),
                    "fetched_at": now, "content_hash": sha(a["content"]), "source_version": "v1",
                })
            url = urljoin(url, d["next"]) if d["next"] else None
        got = sum(r["pcode"] == law["pcode"] for r in rows)
        print(f"  {law['pcode']} {law['name']}：{got}／{law['article_count']}", file=sys.stderr)
        if got != law["article_count"]:
            raise SystemExit(f"{law['pcode']} 筆數不符")
    return rows, expected


def from_html(s: PoliteSession, pcode: str) -> dict[str, str]:
    out, url = {}, BASE + f"v1/laws/{pcode}/"
    while url:
        soup = BeautifulSoup(s.get(url).text, "html.parser")
        for el in soup.select("article.article"):
            out[el["data-slug"]] = "\n".join(p.get_text() for p in el.select(".article-content p"))
        nxt = soup.select_one("a.next")
        url = urljoin(url, nxt["href"]) if nxt else None
    return out


def main():
    s = PoliteSession(BASE)
    print(f"robots.txt OK，間隔 {s.delay} 秒", file=sys.stderr)
    rows, expected = from_api(s)

    pcode = os.environ.get("CHECK_PCODE") or random.choice(sorted(expected))
    html = from_html(s, pcode)
    api = {r["slug"]: r["content"] for r in rows if r["pcode"] == pcode}
    bad = [k for k in api if html.get(k) != api[k]] + [k for k in html if k not in api]
    print(f"HTML 交叉驗證 {pcode}：{len(html)} 條，不一致 {bad or '無'}", file=sys.stderr)
    if bad:
        raise SystemExit("API 與 HTML 不一致")

    with open(OUT, "w", encoding="utf-8") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    print(f"寫入 {OUT}：{len(rows)} 條（{len(expected)} 部法規），共 {s.requests} 個請求")


if __name__ == "__main__":
    main()
