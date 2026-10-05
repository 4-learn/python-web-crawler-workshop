# 規格：職業安全衛生法爬蟲（參考答案）

## 目標
取得爬蟲練習站「職業安全衛生法」（N0060001）全部條文，存成 `osh.jsonl`。

## 來源與方法
- 練習站：https://4-learn.github.io/crawler-playground/
- 使用 API `v1/api/laws/N0060001/page-1.json`，依 `next` 欄位前進；`next` 為 `null` 時停止。
- 網址一律用 `urljoin` 組成，不要自己拼字串。

## 輸出
UTF-8 JSONL，一行一條，`ensure_ascii=False`：
`pcode`、`law_name`、`slug`、`article_no`、`chapter`、`content`、`source_url`（`v1/laws/N0060001/articles/{slug}.html`）、`fetched_at`（ISO 8601，含時區）、`content_hash`（`content` 的 SHA-256）。

## 驗收
1. 條數等於 API 回傳的 `total`（目前 61）；程式中不能寫死 61。
2. `slug` 不重複。
3. 第 1 條內容以「為防止職業災害」開頭。
4. 執行結束印出：條數、第一條與最後一條條號。

## 限制
- 啟動時讀 `robots.txt`；被 Disallow 的網址不得請求。
- 每次請求間隔 ≥ 1 秒；User-Agent：`course-crawler/1.0 (暱稱)`。
- 遇到 429：依 `Retry-After` 等待，最多重試 3 次。
- 只用 `requests`；不要用 Selenium、Playwright。
- 不要修改這份 SPEC.md；不要建立其他檔案以外的輸出。
