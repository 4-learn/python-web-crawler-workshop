# Ch02（改版）參考解答：法規知識蒐集與載入

對應講義〈事件驅動告警系統 Ch02：法規知識蒐集與載入（改版）〉。

學員要在 `event-driven-alert-system` 的 Ch02 基礎上修改；本資料夾放的是**會變動的檔案**：

| 檔案 | 說明 |
|---|---|
| `scraper.py` | 練習站 API → `laws.json`（取代 Selenium 爬 law.moj.gov.tw） |
| `regulation_store.py` | 關鍵字比對，取代固定回傳第一條的 stub |
| `run_system.py` | 示範 4 種事件 |
| `test_ch02.py` | 7 個測試 |

`main.py`（`AlertStateMachine`）沿用原 repo，不修改。

```bash
cp ../../../event-driven-alert-system/main.py .   # 或從 ch-02-knowledge-collection 分支取得
python scraper.py
python run_system.py
pytest -q
```

預期 `run_system.py`：

```text
Loaded 189 regulations
fall       conf=0.92 → ALERTING   第 17 條 雇主對於高度二公尺以上之工作場所…
excavation conf=0.85 → ALERTING   第 64 條 雇主僱用勞工以人工開挖方式…
unknown    conf=0.99 → MONITORING （無）
fall       conf=0.50 → MONITORING （無）
```

（實際條號以執行結果為準，上表於 2026-10-05 驗證。）
