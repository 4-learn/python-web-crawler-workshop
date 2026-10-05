"""09 Workshop 解答：開關卡 3，切換到營造安全衛生設施標準，攔截所有分頁 JSON 存成 JSONL。"""
import json
import os

from playwright.sync_api import sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
PCODE = "N0060014"
pages = {}


def on_response(resp):
    if f"/api/laws/{PCODE}/page-" in resp.url and resp.ok:
        data = resp.json()
        pages[data["page"]] = data


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.on("response", on_response)
    page.goto(BASE + "v1/dynamic/")
    page.locator("article.article").first.wait_for()
    page.select_option("#law-select", value=PCODE)
    page.locator("h2.law-title", has_text="營造安全衛生設施標準").wait_for()
    page.wait_for_function("() => !document.querySelector('#app.loading')")
    browser.close()

total_pages = next(iter(pages.values()))["total_pages"]
assert sorted(pages) == list(range(1, total_pages + 1)), f"缺頁：{sorted(pages)}"
rows = [dict(pcode=PCODE, **a) for n in sorted(pages) for a in pages[n]["articles"]]
with open(f"{PCODE}.jsonl", "w", encoding="utf-8") as f:
    f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
print(f"攔到 {len(pages)} 頁、{len(rows)} 條")
assert len(rows) == pages[1]["total"] == 189
