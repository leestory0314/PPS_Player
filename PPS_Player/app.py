# ---------------------------------------
# Module: app.py
# 위치: PPS_Player/
# 작성 목적: PPS_Player 실행 진입점, 등록 여부 확인 및 메인 UI 실행
# ---------------------------------------
# Version History
# v0.1.0 - 2025.05.01 - 기본 실행 구조 구현
# v0.2.0 - 2025.05.20 - 절대경로 기반 DB 관리 + 등록 체크 기능 추가
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

def is_registered() -> bool:
    """store_info에 등록 정보가 있는지 확인"""
    print("[CHECK] DB 경로:", DB_PATH)

    if not os.path.exists(DB_PATH):
        print("❌ DB 파일 없음")
        return False

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT store_uid FROM store_info LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if row:
            print("✅ 등록 정보 있음:", row[0])
            return row[0].strip() != ""
        else:
            print("❌ 등록 정보 없음")
            return False

    except Exception as e:
        print("❌ DB 확인 오류:", e)
        return False


def run_registration(app: QApplication):
    """등록 UI 실행 → 등록 실패 시 프로그램 종료"""
    popup = RegisterPopup()
    result = popup.exec()
    if result != 1:
        print("❌ 등록 실패 또는 취소됨")
        sys.exit(1)


def main():
    app = QApplication(sys.argv)

    # ✅ DB 마이그레이션 (store_info 테이블 포함)
    migrate_db(DB_PATH)

    # ✅ 등록 확인 후, 없으면 등록창 띄우기
    if not is_registered():
        run_registration(app)

    # ✅ config.json 로드
    config = ConfigManager().load_config()
    print("🛠️ config 로드됨:", config)  # 확인 로그

    # ✅ config 적용하여 메인 실행
    window = MainWindow(config=config)
    window.show()

    sys.exit(app.exec())
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
