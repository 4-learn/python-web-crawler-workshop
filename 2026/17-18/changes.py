"""步驟 3：抓 v2（API 格式不同），與 laws.jsonl 比較 → changes.md、laws.v2.jsonl"""
import hashlib
import json
import os

from polite import PoliteSession

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")


def sha(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def crawl_v2(s):
    rows = []
    for law in s.json(BASE + "v2/api/laws.json")["items"]:
        page = 1
        while True:
            d = s.json(BASE + f"v2/api/laws/{law['code']}/{page}.json")
            rows += [{"pcode": law["code"], "law_name": law["title"], "slug": a["id"], "article_no": a["number"],
                      "chapter": a["chapter"], "content": a["text"],
                      "source_url": BASE + f"v2/laws/{law['code']}/a/{a['id']}.html",
                      "content_hash": sha(a["text"]), "source_version": "v2"} for a in d["items"]]
            if page >= d["pages"]:
                break
            page += 1
        got = sum(r["pcode"] == law["code"] for r in rows)
        assert got == law["articles"], (law["code"], got, law["articles"])
    return rows


def diff(old_rows, new_rows):
    old = {(r["pcode"], r["slug"]): r for r in old_rows}
    new = {(r["pcode"], r["slug"]): r for r in new_rows}
    return (sorted(new.keys() - old.keys()), sorted(old.keys() - new.keys()),
            sorted(k for k in old.keys() & new.keys() if old[k]["content_hash"] != new[k]["content_hash"]), old, new)


def report(added, deleted, modified, old, new) -> str:
    lines = ["# 練習站 v1 → v2 變動報告", "",
             f"| 類型 | 條數 |", "|---|---:|",
             f"| 新增 | {len(added)} |", f"| 刪除 | {len(deleted)} |", f"| 修改 | {len(modified)} |", ""]
    for title, keys, src in [("新增", added, new), ("刪除", deleted, old), ("修改", modified, new)]:
        lines += [f"## {title}", ""]
        lines += [f"- {src[k]['law_name']} {src[k]['article_no']}（`{k[0]}#{k[1]}`）" for k in keys] or ["- 無"]
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    old_rows = [json.loads(l) for l in open("laws.jsonl", encoding="utf-8")]
    new_rows = crawl_v2(PoliteSession(BASE))
    with open("laws.v2.jsonl", "w", encoding="utf-8") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in new_rows)
    added, deleted, modified, old, new = diff(old_rows, new_rows)
    open("changes.md", "w", encoding="utf-8").write(report(added, deleted, modified, old, new))
    print(f"新增 {len(added)}、刪除 {len(deleted)}、修改 {len(modified)} → changes.md")
