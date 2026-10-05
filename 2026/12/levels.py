"""12 Workshop 解答：關卡 3、4、5，並錄一份 trace.zip。"""
import json
import os

from playwright.sync_api import expect, sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")


def level3(context):
    """攔截 JSON：完全不解析 HTML。"""
    pages = {}
    page = context.new_page()
    page.on("response", lambda r: pages.setdefault(r.url, r.json()) if "/api/laws/N0030001/page-" in r.url else None)
    page.goto(BASE + "v1/dynamic/")
    page.wait_for_function("() => !document.querySelector('#app.loading') && document.querySelector('article.article')")
    articles = [a for url in sorted(pages, key=lambda u: pages[u]["page"]) for a in pages[url]["articles"]]
    total = next(iter(pages.values()))["total"]
    assert len(articles) == total, (len(articles), total)
    print(f"關卡 3：攔截 {len(pages)} 頁，勞動基準法 {len(articles)} 條")
    page.close()
    return articles


def level4(context):
    page = context.new_page()
    page.goto(BASE + "v1/scroll/")
    items = page.locator("article.feed-item")
    items.first.wait_for()
    while not page.locator("#feed-end").count():
        n = items.count()
        page.mouse.wheel(0, 4000)
        page.wait_for_function(
            "n => document.querySelectorAll('article.feed-item').length > n || !!document.querySelector('#feed-end')",
            arg=n, timeout=10_000)
    nos = items.locator(".article-no").all_inner_texts()
    assert len(nos) == len(set(nos))
    print(f"關卡 4：捲動取得 {len(nos)} 條（不重複）")
    page.close()
    return nos


def level5(browser):
    if not os.path.exists("state.json"):
        ctx = browser.new_context()
        pg = ctx.new_page()
        pg.goto(BASE + "v1/members/login.html")
        pg.get_by_label("帳號").fill(os.environ["PG_USER"])
        pg.get_by_label("密碼").fill(os.environ["PG_PASS"])
        pg.get_by_role("button", name="登入").click()
        expect(pg.locator("#welcome")).to_be_visible()
        ctx.storage_state(path="state.json")
        ctx.close()
    ctx = browser.new_context(storage_state="state.json")
    pg = ctx.new_page()
    with pg.expect_response(lambda r: "members/notices.json" in r.url) as info:
        pg.goto(BASE + "v1/members/")
    notices = info.value.json()["notices"]
    print(f"關卡 5：{len(notices)} 則會員通知")
    ctx.close()
    return notices


with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True)
    try:
        a3 = level3(context)
        a4 = level4(context)
    finally:
        context.tracing.stop(path="trace.zip")
    n5 = level5(browser)
    browser.close()

with open("levels.json", "w", encoding="utf-8") as f:
    json.dump({"level3": len(a3), "level4": len(a4), "level5": [n["title"] for n in n5]}, f, ensure_ascii=False, indent=1)
