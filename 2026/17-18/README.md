# 17–18 總和 Workshop 參考解答：勞動法規知識蒐集管線

## 執行

```bash
python collect.py                 # → laws.jsonl（749 條）
export DB_USER=crawler DB_PASS=... DB_NAME=crawler_course
python load_db.py laws.jsonl      # 再執行一次，列數不變
python changes.py                 # → laws.v2.jsonl、changes.md
pytest -q
```

約 70 個請求（v1 約 50、v2 約 40），依 `Crawl-delay: 1` 約 1～2 分鐘。

## 每一關選用的工具與理由

| 關卡 | 用途 | 工具 | 理由 |
|---|---|---|---|
| 2 JSON API | 主要資料來源（清單＋條文） | requests | 結構化、有 `total` 可驗證、請求數最少（每頁 20 條） |
| 1 靜態 HTML | 隨機抽 1 部法規交叉驗證 | requests + bs4 | 不需要瀏覽器；用另一個來源抓 API 的錯 |
| 詳細頁 JSON-LD | 測試中抽樣比對 | requests + bs4 | 每條都有 `legislationIdentifier` 可對應 |
| 3 動態／4 捲動 | **不使用** | （Playwright） | 背後就是關卡 2 的 API；開瀏覽器只會更慢、更不穩 |
| 5 會員 | **不使用** | （Playwright） | 通知內容不是條文，與本題無關 |
| 7 v2 改版 | 變動偵測 | requests | v2 也有 API，只是欄位改名、沒有 `next` |
| admin | **禁止** | — | robots.txt Disallow；`PoliteSession` 會直接拒絕 |

評分時接受其他選擇（例如用 Playwright 攔截關卡 3），只要 README 說得出理由、筆數正確、沒碰 admin。
只有「全部用 Playwright 開頁面解析 DOM」而說不出理由的，README 這項不給分。

## 驗收對照

| 項目 | 怎麼看 |
|---|---|
| 749 條且逐條一致 | `test_total_matches_site`、`test_per_law_counts`、`test_sample_against_detail_pages`、collect.py 的 HTML 交叉驗證 |
| 沒碰 admin | 老師 `server.py` 終端機沒有該組的 `[robots]` 紀錄；`test_no_admin_urls` |
| 4／1／1 | `changes.md`、`test_changes_report` |
| 不重複寫入 | `test_db_idempotent` |
