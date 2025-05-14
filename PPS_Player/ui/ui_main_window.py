# PPS_Player/ui/ui_main_window.py
# ---------------------------
# Version History
# v0.2.2 - 2025.04.26 - 모니터 복귀 시 보이지 않는 현상 개선 (move/raise_ 처리)
# ---------------------------

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PPS_Player.core.media_viewer import MediaViewer

class MainWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.is_fullscreen = False
        self.current_screen_index = 0
        self.init_ui()

    def init_ui(self):
        self.resize(1024, 768)
        self.setWindowTitle("PPS 플레이어")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.center_view = QWebEngineView()
        url = self.config.get("url", "https://www.example.com")
        self.center_view.load(QUrl(url))

        media_paths = self.config.get("media_paths", [])
        media_rolling = self.config.get("media_rolling", True)
        bottom_height = self.config.get("bottom_height", 300)

        self.bottom_viewer = MediaViewer(media_paths, rolling=media_rolling)
        self.bottom_viewer.setFixedHeight(bottom_height)

        layout.addWidget(self.center_view)
        layout.addWidget(self.bottom_viewer)
        self.setLayout(layout)

        self.fullscreen_button = QPushButton("전체화면", self)
        self.fullscreen_button.setFixedSize(120, 30)
        self.fullscreen_button.clicked.connect(self.enter_fullscreen)
        self.fullscreen_button.show()

        self.exit_fullscreen_button = QPushButton("일반모드", self)
        self.exit_fullscreen_button.setFixedSize(120, 30)
        self.exit_fullscreen_button.clicked.connect(self.exit_fullscreen)
        self.exit_fullscreen_button.hide()

        self.update_button_position()

        self.mouse_timer = QTimer()
        self.mouse_timer.timeout.connect(self.check_mouse_position)
        self.mouse_timer.start(100)

        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.check_monitor_change)
        self.monitor_timer.start(1000)

    def update_button_position(self):
        x = self.width() - 130
        y = 10
        self.fullscreen_button.move(x, y)
        self.exit_fullscreen_button.move(x, y)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_button_position()

    def enter_fullscreen(self):
        self.showFullScreen()
        self.is_fullscreen = True
        self.fullscreen_button.hide()
        self.exit_fullscreen_button.hide()
        self.bottom_viewer.set_fullscreen(True)

    def exit_fullscreen(self):
        self.showNormal()
        self.is_fullscreen = False
        self.fullscreen_button.show()
        self.exit_fullscreen_button.hide()
        self.bottom_viewer.set_fullscreen(False)

    def check_mouse_position(self):
        if self.is_fullscreen:
            cursor_y = self.mapFromGlobal(self.cursor().pos()).y()
            if cursor_y < 60:
                self.exit_fullscreen_button.show()
            else:
                self.exit_fullscreen_button.hide()
        else:
            self.exit_fullscreen_button.hide()
            self.fullscreen_button.show()

    def check_monitor_change(self):
        screens = QApplication.screens()
        if len(screens) > 1:
            second = screens[1]
            if self.current_screen_index != 1:
                geo = second.geometry()
                print("🖥️ 2번 모니터 감지됨. 전체화면 전환 중...")
                self.move(geo.x(), geo.y())
                self.resize(geo.width(), geo.height())
                self.enter_fullscreen()
                self.current_screen_index = 1
        else:
            primary = QApplication.primaryScreen()
            if self.current_screen_index != 0:
                geo = primary.geometry()
                print("⬅️ 2번 모니터 사라짐. 1번으로 복귀...")
                self.showNormal()
                self.move(geo.x(), geo.y())
                self.resize(1024, 768)
                self.exit_fullscreen()
                self.raise_()  # 🔥 창 최상단으로
                self.activateWindow()  # 🔥 포커스 복원
                self.current_screen_index = 0
