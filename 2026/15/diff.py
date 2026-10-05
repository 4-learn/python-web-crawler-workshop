"""15 Workshop 解答 2/2：比較 v1.jsonl 與 v2.jsonl，輸出 changes.md。"""
import json


def load(path):
    with open(path, encoding="utf-8") as f:
        return {(r["pcode"], r["slug"]): r for r in map(json.loads, f)}


old, new = load("v1.jsonl"), load("v2.jsonl")
added = sorted(new.keys() - old.keys())
deleted = sorted(old.keys() - new.keys())
modified = sorted(k for k in old.keys() & new.keys() if old[k]["content_hash"] != new[k]["content_hash"])

lines = ["# v1 → v2 變動報告", "",
         f"- v1：{len(old)} 條；v2：{len(new)} 條",
         f"- 新增 {len(added)}、刪除 {len(deleted)}、修改 {len(modified)}", ""]
for title, keys, src in [("新增", added, new), ("刪除", deleted, old), ("修改", modified, new)]:
    lines += [f"## {title}", ""]
    lines += [f"- `{p}#{s}` {src[(p, s)]['article_no']}" for p, s in keys] or ["- 無"]
    lines.append("")
open("changes.md", "w", encoding="utf-8").write("\n".join(lines))
print("\n".join(lines))
assert (len(modified), len(deleted), len(added)) == (4, 1, 1)
