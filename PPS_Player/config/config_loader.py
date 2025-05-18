# config/config_loader.py

import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent.parent / "config.json"

DEFAULT_CONFIG = {
    "store_id": "default",
    "store_pw": "default",
    "store_zone_id": "default_zone",
    "store_idx": "",
    "store_z_idx": ""
}

def load_config():
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(json.dumps(DEFAULT_CONFIG, indent=4), encoding="utf-8")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_store_id():
    return load_config().get("store_id", "unknown")

def get_store_pw():
    return load_config().get("store_pw", get_store_id())

def get_store_zone_id():
    return load_config().get("store_zone_id", "")

def get_store_idx():
    return load_config().get("store_idx", "")

def get_store_z_idx():
    return load_config().get("store_z_idx", "")
