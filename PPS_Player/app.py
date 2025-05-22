# ---------------------------------------
# Module: app.py
# 위치: PPS_Player/
# 목적: PPS_Player 실행 진입점 - 등록 여부 확인 및 메인 UI 실행
# ---------------------------------------
# Version History
# v0.3.0 - 2025.05.22 - 로깅 통합, 등록 확인 예외처리 구조화, 중복 코드 제거
# v0.2.0 - 2025.05.20 - 절대경로 기반 DB 관리 + 등록 체크 기능 추가
# v0.1.0 - 2025.05.01 - 기본 실행 구조 구현
# ---------------------------------------

import sys
import os
import sqlite3
from PyQt6.QtWidgets import QApplication

from PPS_Player.config.register_popup import RegisterPopup
from PPS_Player.ui.ui_main_window import MainWindow
from PPS_Player.core.database import migrate_db
from PPS_Player.core.constants import DB_PATH
from PPS_Player.config.config_manager import ConfigManager
from PPS_Player.common.logger import setup_logger

logger = setup_logger()


def is_registered() -> bool:
    """
    로컬 DB(store_info)에 등록된 store_uid 존재 여부 확인
    """
    logger.info(f"[CHECK] DB 경로: {DB_PATH}")

    if not os.path.exists(DB_PATH):
        logger.warning("❌ DB 파일 없음")
        return False

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT store_uid FROM store_info LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if row and row[0].strip():
            logger.info(f"✅ 등록 정보 있음: {row[0]}")
            return True
        else:
            logger.warning("❌ 등록 정보 없음")
            return False

    except Exception as e:
        logger.exception("❌ DB 확인 중 오류")
        return False


def run_registration(app: QApplication):
    """
    등록 UI 실행 → 등록 실패 시 프로그램 종료
    """
    popup = RegisterPopup()
    result = popup.exec()
    if result != 1:
        logger.warning("❌ 등록 실패 또는 취소됨")
        sys.exit(1)


def main():
    """
    앱 진입점 - 등록 확인 후 config 로드 및 메인 UI 실행
    """
    logger.info("▶ PPS_Player 실행 시작")
    app = QApplication(sys.argv)

    # DB 마이그레이션
    migrate_db(DB_PATH)

    # 등록 여부 확인
    if not is_registered():
        run_registration(app)

    # config.json 로드
    try:
        config = ConfigManager().load_config()
    except Exception as e:
        logger.critical("⛔ config 로딩 실패. 앱 종료")
        sys.exit(1)

    # 메인 UI 실행
    window = MainWindow(config=config)
    window.show()

    logger.info("✅ PPS_Player UI 시작됨")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
