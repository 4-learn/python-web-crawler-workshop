"""步驟 2：laws.jsonl 寫入 MariaDB（upsert，重複執行不重複）。

export DB_USER=... DB_PASS=... DB_NAME=crawler_course [DB_HOST DB_PORT]
python load_db.py laws.jsonl
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
  law_name = VALUES(law_name), article_no = VALUES(article_no), chapter = VALUES(chapter),
  content = VALUES(content), source_url = VALUES(source_url), source_version = VALUES(source_version),
  fetched_at = IF(content_hash = VALUES(content_hash), fetched_at, VALUES(fetched_at)),
  content_hash = VALUES(content_hash)
"""


def connect():
    return mariadb.connect(host=os.environ.get("DB_HOST", "127.0.0.1"), port=int(os.environ.get("DB_PORT", 3306)),
                           user=os.environ["DB_USER"], password=os.environ["DB_PASS"],
                           database=os.environ.get("DB_NAME", "crawler_course"))


def load(path: str) -> int:
    rows = [json.loads(l) for l in open(path, encoding="utf-8")]
    params = [(r["pcode"], r["law_name"], r["slug"], r["article_no"], r["chapter"], r["content"], r["source_url"],
               r.get("source_version", "v1"), r["content_hash"],
               dt.datetime.fromisoformat(r.get("fetched_at") or dt.datetime.now(dt.timezone.utc).isoformat())
               .astimezone(dt.timezone.utc).replace(tzinfo=None)) for r in rows]
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute(DDL)
        cur.executemany(UPSERT, params)
        conn.commit()
        cur.execute("SELECT COUNT(*), COUNT(DISTINCT pcode, slug) FROM law_articles")
        total, distinct = cur.fetchone()
        print(f"讀入 {len(rows)} 筆；資料表 {total} 列（不重複 {distinct}）")
        return total
    except mariadb.Error:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    load(sys.argv[1] if len(sys.argv) > 1 else "laws.jsonl")
