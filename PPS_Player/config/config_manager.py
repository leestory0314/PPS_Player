# PPS_Player/config/config_manager.py
# ---------------------------
# Version History
# v0.1.0 - 2025.04.25 - 기본 config 로딩 클래스 생성
# v0.2.0 - 2025.04.26 - PyInstaller 대응을 위한 base_path 처리 추가
# ---------------------------

import json
import os
import sys

class ConfigManager:
    def __init__(self):
        self.config_path = self.get_default_config_path()

    def get_default_config_path(self):
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, '..', 'config.json')

    def load_config(self, path=None):
        config_file = path or self.config_path
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {config_file}")

        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
