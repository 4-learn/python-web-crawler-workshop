"""08 Workshop 解答：不用 sleep，依序切換 3 部法規，記錄條數；最後與 API 比對。"""
import os

import requests
from playwright.sync_api import expect, sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
TARGETS = ["勞動基準法", "性別平等工作法", "大量解僱勞工保護法"]

result = {}
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(BASE + "v1/dynamic/")
    title = page.locator("h2.law-title")
    for name in TARGETS:
        page.get_by_label("選擇法規").select_option(label=name)
        expect(title).to_contain_text(name)
        expect(page.locator("#app")).not_to_have_class("loading")
        result[name] = page.locator("article.article").count()
        print(title.inner_text(), "→", result[name])
    browser.close()

api = {l["name"]: l["article_count"] for l in requests.get(BASE + "v1/api/laws.json", timeout=10).json()["laws"]}
for name, n in result.items():
    assert n == api[name], (name, n, api[name])
print("全部與 API 一致")
