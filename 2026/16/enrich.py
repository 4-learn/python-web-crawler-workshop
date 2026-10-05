"""16 Workshop 解答 1/2：把第 05 節的 labor_standards.jsonl 補上下游需要的欄位。

python enrich.py ../05/labor_standards.jsonl > labor_standards.v1.jsonl
"""
import datetime as dt
import hashlib
import json
import sys

now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
for line in open(sys.argv[1], encoding="utf-8"):
    r = json.loads(line)
    r.setdefault("fetched_at", now)
    r["content_hash"] = hashlib.sha256(r["content"].encode("utf-8")).hexdigest()
    r["source_version"] = "v1"
    print(json.dumps(r, ensure_ascii=False))
