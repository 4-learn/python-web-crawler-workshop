"""12 Workshop 解答：關卡 3、4、5，並錄一份 output/trace.zip（不含登入）。"""
import json
import os

from playwright.sync_api import expect, sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
os.makedirs("output", exist_ok=True)
STATE = "output/state.json"   # 內含 cookie，等同登入憑證：不要 commit


def level3(context):
    """攔截 JSON：條文完全來自 API 回應，不解析 HTML（第 09 節）。"""
    pages = {}

    def log(resp):
        if "/api/laws/N0030001/page-" in resp.url and resp.ok:
            data = resp.json()
            pages[data["page"]] = data

    page = context.new_page()
    page.on("response", log)
    page.goto(BASE + "v1/dynamic/")
    expect(page.locator("h2.law-title")).to_contain_text("勞動基準法")
    expect(page.locator("#app")).not_to_have_class("loading")

    total_pages = pages[1]["total_pages"]
    assert sorted(pages) == list(range(1, total_pages + 1)), f"缺頁：{sorted(pages)}"
    articles = []
    for n in sorted(pages):
        articles += pages[n]["articles"]
    assert len(articles) == pages[1]["total"], (len(articles), pages[1]["total"])
    print(f"關卡 3：攔截 {len(pages)} 頁，勞動基準法 {len(articles)} 條")
    page.close()
    return articles


def level4(context):
    """捲動到出現 #feed-end，每次等下一條出現（第 10 節）。"""
    page = context.new_page()
    page.goto(BASE + "v1/scroll/")
    items = page.locator("article.feed-item")
    items.first.wait_for()
    rounds = 0
    while page.locator("#feed-end").count() == 0 and rounds < 50:
        before = items.count()
        page.mouse.wheel(0, 3000)
        expect(items.nth(before)).to_be_attached(timeout=10_000)
        rounds += 1
    numbers = items.locator(".article-no").all_inner_texts()
    assert len(numbers) == len(set(numbers)), "條號有重複"
    print(f"關卡 4：捲動取得 {len(numbers)} 條（不重複）")
    page.close()
    return numbers


def level5(browser):
    """表單登入一次、存 storage_state，之後重用；登入過程不錄進 trace（第 10、12 節）。"""
    if not os.path.exists(STATE):
        context = browser.new_context()
        page = context.new_page()
        page.goto(BASE + "v1/members/login.html")
        page.get_by_label("帳號").fill(os.environ["PG_USER"])
        page.get_by_label("密碼").fill(os.environ["PG_PASS"])
        page.get_by_role("button", name="登入").click()
        expect(page.locator("#welcome")).to_be_visible()
        context.storage_state(path=STATE)
        context.close()
    context = browser.new_context(storage_state=STATE)
    page = context.new_page()
    page.goto(BASE + "v1/members/")
    notices = page.locator("li.notice-item")
    notices.first.wait_for()
    titles = notices.all_inner_texts()
    print(f"關卡 5：{len(titles)} 則會員通知")
    context.close()
    return titles


with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True)
    try:
        a3 = level3(context)
        a4 = level4(context)
    finally:
        context.tracing.stop(path="output/trace.zip")   # 只錄關卡 3、4，不含登入
    t5 = level5(browser)
    browser.close()

with open("output/levels.json", "w", encoding="utf-8") as f:
    json.dump({"level3": len(a3), "level4": len(a4), "level5": t5}, f, ensure_ascii=False, indent=1)
