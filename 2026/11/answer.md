# 11 Workshop 參考解答

## 1. 用 Trace 找錯

`trace_demo.py` 的錯誤：`page.locator("tr.row")` 是 v2 的條文選擇器，v1 動態頁面上是 `article.article`。

在 `playwright show-trace trace.zip`：
- **Actions** 面板：`locator.wait_for` 紅色、Timeout 3000ms。
- **Snapshot**（Before/After）：畫面已經有條文，代表不是「還沒載入」。
- 點 DOM 快照中的條文 → 看到 `<article class="article">`，修正 selector。

## 2. Selenium → Playwright 對照

| 舊講義（Selenium） | Playwright |
|---|---|
| `webdriver.Chrome(ChromeDriverManager().install())` | `p.chromium.launch()`（`playwright install` 一次） |
| `driver.get(url)` | `page.goto(url)` |
| `WebDriverWait(d,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, s)))` | `page.locator(s).first.wait_for()`；或不寫，動作本身會自動等待 |
| `driver.find_element(By.ID, "username").send_keys("x")` | `page.fill("#username", "x")` |
| `driver.find_elements(By.CLASS_NAME, "row")` | `page.locator(".row").all()` |
| `driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")` | `page.mouse.wheel(0, 3000)` |
| `driver.quit()` | `browser.close()` |

Selenium 4.6 起內建 Selenium Manager，不再需要 `webdriver_manager`。

## 3. 什麼時候還會用 Selenium？

- 公司既有測試已用 Selenium／Selenium Grid。
- 需要特定瀏覽器版本或 Appium（行動裝置）。
- 爬蟲新專案：優先 API → requests → Playwright。
