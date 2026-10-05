# 02 Workshop 參考解答：關卡 3 背後的請求

DevTools → Network → 篩選 **Fetch/XHR** → 重新整理 `v1/dynamic/`：

| 請求 | Status | 用途 |
|---|---|---|
| `v1/api/laws.json` | 200 | 下拉選單的法規清單 |
| `v1/api/laws/N0030001/page-1.json` … `page-5.json` | 200 | 勞動基準法 98 條，每頁 20 條 |

點開任一請求：
- **Headers**：Request Method `GET`、Content-Type `application/json`
- **Response**：有 `next` 欄位（`page-2.json`），最後一頁為 `null`

結論：這些 JSON 可以直接用 requests 取得（第 03 節），不必開瀏覽器。

切換下拉選單到「職業安全衛生法」會再出現 `N0060001/page-1.json` ～ `page-4.json`。
