# 06 Workshop 驗收

1. 沒禮貌版：30 次中約 10 次 `429`（教室版預設 burst 20、每秒 5 次）。
2. 有禮貌版：全部 `200`；`v1/admin/` 被跳過。
3. 老師終端機不應出現該學員 IP／UA 的 `[robots]` 紀錄。

常見錯誤：
- 用 `RobotFileParser.read()`：robots.txt 本身被 429 時，Python 會把它當成「全部允許」（3.10 行為：401/403 → 全禁，其餘 4xx → 全允許）。被限速時更要自己下載再 `parse()`。
- 重試時沒有讀 `Retry-After`，固定 sleep 太短又被擋。
