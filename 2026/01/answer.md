# 01 Workshop 參考解答：能不能爬？

| 網站 | robots.txt 重點 | 能不能爬 | 理由／替代管道 |
|---|---|---|---|
| 爬蟲練習站 | `Disallow: .../v1/admin/`、`.../v2/admin/`、`Crawl-delay: 1`、`BadBot` 全禁 | 可以，但避開 admin、每秒最多 1 次 | 本課練習用 |
| 全國法規資料庫 law.moj.gov.tw | `User-agent: *` / `Disallow: /` | **不行** | 改用官方開放資料 API（`/api/Ch/Law/JSON`），法條不受著作權保護（著作權法第 9 條） |
| 勞動部 www.mol.gov.tw | 只禁 `/bin/*`、`/App_Data/*`、`/Umbraco/*` 等後台路徑 | 公開頁面技術上允許 | 仍須看網站服務條款；統計資料優先找政府資料開放平台 |
| 社群平台（例：Facebook） | 大量 Disallow，條款明文禁止未經許可的自動化蒐集 | **不行** | 會被封號；有官方 API 也需審核，且涉及個資 |

判斷順序：有沒有官方 API／開放資料 → robots.txt → 服務條款 → 資料是否含個資或受著作權保護 → 速率與身分（User-Agent）。

> robots.txt 會變動，上課前請老師重新確認實際內容。
