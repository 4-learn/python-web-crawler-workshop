"""共用：遵守 robots.txt、Crawl-delay 與 429 Retry-After 的 HTTP 客戶端。"""
import time
import urllib.robotparser
from urllib.parse import urljoin

import requests


class Blocked(Exception):
    pass


class PoliteSession:
    def __init__(self, base: str, user_agent: str = "course-crawler/1.0 (team-teacher)"):
        self.base, self.ua = base, user_agent
        self.s = requests.Session()
        self.s.headers["User-Agent"] = user_agent
        self._last = 0.0
        self.requests = 0
        self.robots = urllib.robotparser.RobotFileParser()
        r = self._raw(urljoin(base, "robots.txt"), check=False)
        if r.status_code == 404:
            self.robots.allow_all = True
        elif r.status_code != 200:
            raise Blocked(f"robots.txt 回 {r.status_code}，保守起見停止")
        else:
            r.encoding = "utf-8"
            self.robots.parse(r.text.splitlines())
        self.delay = float(self.robots.crawl_delay(user_agent) or 1)

    def _raw(self, url: str, check: bool = True) -> requests.Response:
        if check and not self.robots.can_fetch(self.ua, url):
            raise Blocked(f"robots.txt 不允許：{url}")
        for attempt in range(5):
            wait = getattr(self, "delay", 1.0) - (time.monotonic() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.monotonic()
            r = self.s.get(url, timeout=15)
            self.requests += 1
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(float(r.headers.get("Retry-After", 2 ** attempt)))
                continue
            return r
        raise Blocked(f"重試後仍失敗：{url}")

    def get(self, url: str) -> requests.Response:
        r = self._raw(url)
        r.raise_for_status()
        r.encoding = "utf-8"
        return r

    def json(self, url: str):
        return self.get(url).json()
