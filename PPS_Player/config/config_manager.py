# ---------------------------------------
# Module: config_manager.py
# 위치: PPS_Player/config/
# 목적: config.json 로드 및 경로 관리
# ---------------------------------------
# Version History
# v0.3.0 - 2025.05.22 - 로깅 연동, 파일 존재 검증 및 오류 로그 처리
# v0.2.0 - 2025.04.26 - PyInstaller 대응을 위한 base_path 처리 추가
# v0.1.0 - 2025.04.25 - 기본 config 로딩 클래스 생성
# ---------------------------------------

import json
import os

from PPS_Player.common.logger import setup_logger

logger = setup_logger()


class ConfigManager:
    """
    config.json 파일 로더
    """
    def __init__(self, path=None):
        self.config_path = path or self.get_default_config_path()

    def get_default_config_path(self):
        """
        PyInstaller 대응을 포함한 기본 경로 추출
        """
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        return os.path.join(base_path, 'config.json')

    def load_config(self):
        """
        config.json 파일을 로드하여 dict로 반환
        """
        if not os.path.exists(self.config_path):
            logger.error(f"설정 파일 없음: {self.config_path}")
            raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {self.config_path}")

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                logger.info(f"✅ config 로드 성공: {self.config_path}")
                return config
        except Exception as e:
            logger.exception("❌ config 로드 중 오류 발생")
            raise
