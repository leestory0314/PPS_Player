# PPS_Player/config/config_manager.py
# ---------------------------
# Version History
# v0.0.1 - 2025.04.25 - 최초 작성: config.json 로딩 기능 구현
# v0.1.0 - 2025.04.26 - config.json 미존재 시 기본값 반환 기능 추가
# ---------------------------

import json
import os

DEFAULT_CONFIG = {
    "store_id": "store_test_001",
    "top_notice_text": "매장명 / 연락처: 010-0000-0000",
    "url": "https://www.example.com",
    "media_paths": [],
    "music_paths": [],
    "music_play_mode": "loop",
    "polling_interval": 5
}

class ConfigManager:
    def __init__(self, path="config.json"):
        self.path = path

    def load_config(self):
        if not os.path.isfile(self.path):
            print(f"[⚠️ config.json 미존재] 기본 설정으로 실행합니다: {self.path}")
            return DEFAULT_CONFIG

        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[⚠️ config.json 읽기 오류] 기본 설정으로 실행합니다: {e}")
            return DEFAULT_CONFIG
