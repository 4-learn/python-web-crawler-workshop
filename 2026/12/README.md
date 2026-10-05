# 12 Workshop 參考解答：動態關卡實戰

| 關卡 | 方法 | 為什麼 |
|---|---|---|
| 3 動態載入 | **攔截 JSON**（`page.on("response")`） | 資料本來就是 JSON，有 `total`；比解析 DOM 穩，版面改了也不受影響 |
| 4 無限捲動 | **捲動 + locator**；以 `#feed-end` 為終止條件 | 要模擬使用者捲動才會觸發載入；終止條件明確 |
| 5 會員登入 | **表單登入 + `storage_state`** | 只登入一次；後續 context 重用 cookie |

另一種合理做法：關卡 4 也可攔截 `v1/api/feed/page-N.json`，直到 `has_more` 為 `false`。

執行：

```bash
export PG_USER=student PG_PASS=crawler-demo
python levels.py
playwright show-trace trace.zip
```

預期：

```text
關卡 3：攔截 5 頁，勞動基準法 98 條
關卡 4：捲動取得 98 條（不重複）
關卡 5：5 則會員通知
```
