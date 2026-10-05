"""07 Workshop 解答：用 Playwright 取得關卡 3 中「職業安全衛生法」的標題與條數，並截圖。"""
import os

from playwright.sync_api import sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(user_agent="course-crawler/1.0 (teacher)")
    page.goto(BASE + "v1/dynamic/")
    page.locator("article.article").first.wait_for()
    page.select_option("#law-select", label="職業安全衛生法")
    page.locator("h2.law-title", has_text="職業安全衛生法").wait_for()
    title = page.locator("h2.law-title").inner_text()
    n = page.locator("article.article").count()
    page.screenshot(path="osh.png")
    browser.close()

print(title, "→ 頁面上", n, "條")
assert n == 61
