"""11 Workshop 解答：修正後的 trace_demo。

執行：python trace_demo.py
查看：playwright show-trace trace.zip   （或上傳到 https://trace.playwright.dev ，檔案只在本機瀏覽器處理）
"""
import os

from playwright.sync_api import sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    try:
        page.goto(BASE + "v1/dynamic/")
        page.locator("article.article").first.wait_for(timeout=3000)
        print("找到", page.locator("article.article").count(), "條")
    except Exception as e:
        print("失敗了：", type(e).__name__)
        print("打開 trace.zip 看失敗當下的畫面與 DOM")
    finally:
        context.tracing.stop(path="trace.zip")
        browser.close()
