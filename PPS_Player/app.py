# PPS_Player/app.py
# ---------------------------
# Version History
# v0.0.2 - 전체화면 제거 후 일반모드 실행
# ---------------------------

import sys
from PyQt5.QtWidgets import QApplication
from PPS_Player.config.config_manager import ConfigManager
from PPS_Player.ui.ui_main_window import MainWindow

def main():
    config = ConfigManager().load_config()
    app = QApplication(sys.argv)

    window = MainWindow(config)
    window.show()  # ✅ 무조건 있어야 UI가 뜬다

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
