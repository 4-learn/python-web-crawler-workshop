"""16 Workshop 解答 2/2：寫入 MariaDB law_articles；重複執行不重複。

export DB_USER=... DB_PASS=... DB_NAME=crawler_course [DB_HOST DB_PORT]
python load.py labor_standards.v1.jsonl
"""
import datetime as dt
import json
import os
import sys

import mariadb

DDL = """
CREATE TABLE IF NOT EXISTS law_articles (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  pcode VARCHAR(16) NOT NULL, law_name VARCHAR(100) NOT NULL, slug VARCHAR(16) NOT NULL,
  article_no VARCHAR(32) NOT NULL, chapter VARCHAR(200) NOT NULL DEFAULT '', content TEXT NOT NULL,
  source_url VARCHAR(500) NOT NULL, source_version VARCHAR(8) NOT NULL DEFAULT 'v1',
  content_hash CHAR(64) NOT NULL, fetched_at DATETIME NOT NULL,
  UNIQUE KEY uk_article (pcode, slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
"""
UPSERT = """
INSERT INTO law_articles (pcode, law_name, slug, article_no, chapter, content, source_url,
                          source_version, content_hash, fetched_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON DUPLICATE KEY UPDATE
  article_no = IF(content_hash = VALUES(content_hash), article_no, VALUES(article_no)),
  chapter    = IF(content_hash = VALUES(content_hash), chapter, VALUES(chapter)),
  content    = IF(content_hash = VALUES(content_hash), content, VALUES(content)),
  source_version = VALUES(source_version),
  fetched_at = IF(content_hash = VALUES(content_hash), fetched_at, VALUES(fetched_at)),
  content_hash = VALUES(content_hash)
"""


def to_dt(s):
    return dt.datetime.fromisoformat(s).astimezone(dt.timezone.utc).replace(tzinfo=None)


rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
conn = mariadb.connect(host=os.environ.get("DB_HOST", "127.0.0.1"), port=int(os.environ.get("DB_PORT", 3306)),
                       user=os.environ["DB_USER"], password=os.environ["DB_PASS"],
                       database=os.environ.get("DB_NAME", "crawler_course"))
try:
    cur = conn.cursor()
    cur.execute(DDL)
    # 第 16 節示範的 schema.sql 沒有 source_version：舊表就補上欄位
    cur.execute("SHOW COLUMNS FROM law_articles LIKE 'source_version'")
    if not cur.fetchall():
        cur.execute("ALTER TABLE law_articles ADD COLUMN source_version VARCHAR(8) NOT NULL DEFAULT 'v1'")
    cur.execute("SELECT COUNT(*) FROM law_articles")
    before = cur.fetchone()[0]
    cur.executemany(UPSERT, [(r["pcode"], r["law_name"], r["slug"], r["article_no"], r["chapter"], r["content"],
                              r["source_url"], r.get("source_version", "v1"), r["content_hash"], to_dt(r["fetched_at"]))
                             for r in rows])
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM law_articles")
    after = cur.fetchone()[0]
    cur.execute("SELECT pcode, COUNT(*), COUNT(DISTINCT slug) FROM law_articles GROUP BY pcode")
    print(f"執行前 {before} 列，執行後 {after} 列（本次 {len(rows)} 筆）")
    for p, n, d in cur.fetchall():
        print(" ", p, n, "列，不重複 slug", d)
except mariadb.Error:
    conn.rollback()
    raise
finally:
    conn.close()
