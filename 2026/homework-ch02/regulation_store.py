"""Ch02（改版）RegulationStore：依關鍵字回傳相關條文，取代「固定回傳第一條」的 stub。"""
from typing import Dict, List, Optional

# 事件類型 → 關鍵字（依序比對，越前面越優先）
EVENT_KEYWORDS: Dict[str, List[str]] = {
    "fall": ["墜落"],
    "excavation": ["開挖"],
    "intrusion": ["禁止", "進入"],
    "collapse": ["崩塌", "倒塌"],
}


class RegulationStore:
    def __init__(self, laws: List[Dict]):
        self.laws = laws

    def list_articles(self) -> List[str]:
        return [law.get("article_number") for law in self.laws]

    def search(self, keywords: List[str], limit: int = 5) -> List[Dict]:
        """全部關鍵字都出現的條文；依出現次數排序，同分保持原順序。"""
        if not keywords:
            return []
        scored = []
        for i, law in enumerate(self.laws):
            text = law.get("content", "")
            if all(k in text for k in keywords):
                scored.append((-sum(text.count(k) for k in keywords), i, law))
        return [law for _, _, law in sorted(scored, key=lambda t: t[:2])[:limit]]

    def match_event(self, event: Dict) -> Optional[Dict]:
        keywords = event.get("keywords") or EVENT_KEYWORDS.get(event.get("type", ""), [])
        hits = self.search(keywords, limit=1)
        return hits[0] if hits else None
