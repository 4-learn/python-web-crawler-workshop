import json

from main import AlertStateMachine
from regulation_store import RegulationStore

with open("laws.json", "r", encoding="utf-8") as f:
    laws = json.load(f)

store = RegulationStore(laws)
print(f"Loaded {len(store.list_articles())} regulations")

for event in [
    {"source": "camera_01", "type": "fall", "confidence": 0.92},
    {"source": "camera_02", "type": "excavation", "confidence": 0.85},
    {"source": "camera_03", "type": "unknown", "confidence": 0.99},
    {"source": "camera_04", "type": "fall", "confidence": 0.50},
]:
    system = AlertStateMachine(store)
    system.start_monitoring()
    system.handle_event(event)
    law = system.last_triggered_law
    hit = f"{law['article_number']} {law['content'][:30]}…" if law else "（無）"
    print(f"{event['type']:<10} conf={event['confidence']:.2f} → {system.state:<10} {hit}")
