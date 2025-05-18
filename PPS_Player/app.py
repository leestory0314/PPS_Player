# PPS_Player/app.py
# ---------------------------
# Version History
# v0.1.0 - 2025.04.25 - 초기 앱 진입점 생성
# v0.2.0 - 2025.04.26 - config.json 없을 경우 기본 생성 추가
# v0.2.3 - 2025.04.26 - 디버깅 로그 시스템 추가 (logs/YYYY-MM-DD.log)
# v0.2.4 - 2025.04.26 - 경로 처리 통일 (PyInstaller 대비 get_base_path 적용)
# v0.3.0 - 2025.05.15 - PyQt6 호환 구조로 전환
# ---------------------------

import sys
import os
import json
import logging
from datetime import datetime
from PyQt6.QtWidgets import QApplication
from PPS_Player.config.config_manager import ConfigManager
from PPS_Player.ui.ui_main_window import MainWindow

# ✅ base 경로 함수 정의 (PyInstaller 대응)
def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()

# ✅ 로그 디렉토리 설정
now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
month_folder = now.strftime("%Y-%m")
log_dir = os.path.join(BASE_PATH, "logs", month_folder)
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, f"{date_str}.log")

# ✅ 로깅 설정
logging.basicConfig(
    filename=log_path,
    filemode="a",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logging.info("💡 PPS_Player 실행 시작")

# ✅ config.json 자동 생성 로직
CONFIG_PATH = os.path.join(BASE_PATH, "config.json")
if not os.path.exists(CONFIG_PATH):
    logging.warning("⚠️ config.json 없음. 기본값으로 생성합니다.")
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "url": "https://www.naver.com",
            "media_paths": [],
            "bottom_height": 300,
            "media_rolling": True
        }, f, indent=2)

# ✅ 애플리케이션 진입점
def main():
    try:
        config = ConfigManager().load_config(CONFIG_PATH)
        app = QApplication(sys.argv)
        window = MainWindow(config)
        window.show()
        sys.exit(app.exec())  # ✅ PyQt6는 exec_() → exec()
    except Exception as e:
        logging.exception("🚨 예외 발생:")
        raise

if __name__ == "__main__":
    main()