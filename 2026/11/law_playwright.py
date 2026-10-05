"""11 Workshop B 解答：把舊版 Selenium 法規爬蟲改寫成 Playwright，改爬練習站。

舊版需求：章節、條文編號、條文連結、條文內容 → laws_data.json
"""
import json
import os
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
URL = BASE + "v1/laws/N0030001/"

rows = []
with sync_playwright() as p:
    browser = p.chromium.launch()                                   # 舊：webdriver.Chrome(...)
    page = browser.new_page(user_agent="course-crawler/1.0 (teacher)")
    url = URL
    while url:
        page.goto(url)                                              # 舊：driver.get(url)
        articles = page.locator("article.article")                  # 舊：find_elements(By.CLASS_NAME, "row")
        articles.first.wait_for()                                   # 舊：WebDriverWait(...).until(...)
        for el in articles.all():
            link = el.locator(".article-no a")
            rows.append({
                "chapter": el.locator(".chapter").inner_text().strip(),
                "article_number": link.inner_text().strip(),
                "article_link": urljoin(url, link.get_attribute("href")),
                "content": "\n".join(el.locator(".article-content p").all_inner_texts()),
            })
        nxt = page.locator("a.next")
        url = urljoin(url, nxt.get_attribute("href")) if nxt.count() else None
        page.wait_for_timeout(1000)                                 # Crawl-delay: 1
    browser.close()                                                 # 舊：driver.quit()

with open("laws_data.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
chapters = list(dict.fromkeys(r["chapter"] for r in rows))
print(f"共 {len(rows)} 條、{len(chapters)} 個章節")
print(rows[0]["chapter"], "|", rows[0]["article_number"])
assert len(rows) == 98 and len(chapters) == 12
