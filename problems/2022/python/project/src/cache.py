import json
import os

CACHE_DIR = ".cache"

def _ensure_cache_dir():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def save_json(filename: str, data: dict):
    _ensure_cache_dir()
    path = os.path.join(CACHE_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f)

def load_json(filename: str):
    path = os.path.join(CACHE_DIR, filename)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None
