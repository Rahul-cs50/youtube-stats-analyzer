import json
from pathlib import Path

CACHE_DIR = Path('cache')
CACHE_DIR.mkdir(exist_ok=True)

def save_json(name: str, obj: dict):
    p = CACHE_DIR / (name + '.json')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def load_json(name: str):
    p = CACHE_DIR / (name + '.json')
    if not p.exists():
        return None
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)