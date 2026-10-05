"""10 Workshop 解答：
A. 捲完關卡 4，確認 98 條、無重複，與 API feed 一致。
B. 登入關卡 5，保存 state.json，再用它取會員通知。
帳密：export PG_USER=student PG_PASS=crawler-demo
"""
import os
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
STATE = Path("state.json")

with sync_playwright() as p:
    browser = p.chromium.launch()

    # A. 無限捲動
    page = browser.new_page()
    page.goto(BASE + "v1/scroll/")
    items = page.locator("article.feed-item")
    items.first.wait_for()
    while not page.locator("#feed-end").count():
        n = items.count()
        page.locator("#sentinel").scroll_into_view_if_needed()
        page.wait_for_function(
            "n => document.querySelectorAll('article.feed-item').length > n || !!document.querySelector('#feed-end')",
            arg=n, timeout=10_000)
    nos = items.locator(".article-no").all_inner_texts()
    print("A. 捲動取得", len(nos), "條，不重複", len(set(nos)), "條")
    assert len(nos) == len(set(nos)) == 98

    # B. 登入
    if not STATE.exists():
        ctx = browser.new_context()
        pg = ctx.new_page()
        pg.goto(BASE + "v1/members/login.html")
        pg.fill("#username", os.environ["PG_USER"])
        pg.fill("#password", os.environ["PG_PASS"])
        pg.click("#login-button")
        expect(pg.locator("#welcome")).to_be_visible()
        ctx.storage_state(path=STATE)
        ctx.close()
    ctx = browser.new_context(storage_state=STATE)
    pg = ctx.new_page()
    pg.goto(BASE + "v1/members/")
    expect(pg.locator("#member-name")).not_to_be_empty()
    pg.locator("li.notice-item").first.wait_for()
    notices = pg.locator("li.notice-item").all_inner_texts()
    print("B.", pg.locator("#member-name").inner_text(), "有", len(notices), "則通知")
    browser.close()
