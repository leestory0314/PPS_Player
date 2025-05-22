# ---------------------------------------
# Module: logger.py
# 위치: PPS_Player/common/
# 목적: 로그 출력 및 저장 (PPS_Player/logs/ 하위로 고정 생성)
# ---------------------------------------
# Version History
# v0.3.0 - 2025.05.22 - 로그 저장 경로를 프로젝트 내부 logs/ 디렉토리로 고정
# v0.2.0 - 2025.05.22 - 중복 핸들러 방지 및 경로 확인 강화
# v0.1.0 - 2025.05.15 - 기본 로거 구성
# ---------------------------------------

import logging
import os
from datetime import datetime

def setup_logger(name="PPS_Player"):
    """
    logs/YYYY-MM/날짜.log 파일로 고정 저장하는 로거 생성
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # ✅ 중복 초기화 방지

    # 기준 경로를 현재 파일 위치 기준으로 고정
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    today = datetime.now().strftime("%Y-%m-%d")
    log_month = today[:7]  # YYYY-MM

    log_dir = os.path.join(base_path, "logs", log_month)
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"{today}.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.propagate = False

    return logger
