# ---------------------------------------
# Module: ui_main_window.py
# 위치: PPS_Player/ui/
# 목적: 메인 UI - Header + WebView + MediaViewer + 상태 기반 float 버튼
# ---------------------------------------
# Version History
# v0.5.3 - 2025.05.22 - 버튼 조건부 표시 및 투명 스타일 완전 적용
# ---------------------------------------

from PyQt6.QtCore import Qt, QTimer, QUrl, QPoint
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QApplication, QSizePolicy
)
from PyQt6.QtGui import QKeyEvent, QGuiApplication

from PPS_Player.core.media_viewer import MediaViewer
from PPS_Player.ui.header_widget import HeaderWidget
from PPS_Player.common.logger import setup_logger
import pyttsx3

logger = setup_logger()


class CustomWebPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        if msg.startswith("TTS:"):
            text = msg[4:].strip()
            if self.parent() and hasattr(self.parent(), "tts_engine"):
                self.parent().tts_engine.say(text)
                self.parent().tts_engine.runAndWait()


class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.debug_layout = self.config.get("debug_layout", False)
        self.is_fullscreen = False
        self.current_screen_index = -1
        self.tts_engine = pyttsx3.init()

        self.init_ui()
        QTimer.singleShot(0, self.setFocus)

    def init_ui(self):
        self.setWindowTitle("PPS 플레이어")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setStyleSheet("background-color: #111111;")

        screen_geo = QGuiApplication.primaryScreen().availableGeometry()
        self.resize(screen_geo.width(), screen_geo.height())

        self.main_layout = QVBoxLayout()
        self.header = HeaderWidget(self.config)
        self.main_layout.addWidget(self.header)

        self.center_view = QWebEngineView()
        self.center_page = CustomWebPage(self.center_view)
        self.center_view.setPage(self.center_page)
        self.center_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.center_view.load(QUrl(self.config.get("url")))
        self.main_layout.addWidget(self.center_view, stretch=1)

        interval = max(self.config.get("web_refresh_interval", 20000), 5000)
        self.js_timer = QTimer()
        self.js_timer.timeout.connect(
            lambda: self.center_view.page().runJavaScript(
                "if (typeof dashboard_update === 'function') requestAnimationFrame(() => dashboard_update());"
            )
        )
        self.js_timer.start(interval)

        self.bottom_viewer = MediaViewer(
            self.config.get("media_paths", []),
            rolling=self.config.get("media_rolling", False),
            debug=self.debug_layout
        )
        self.bottom_viewer.setFixedHeight(self.config.get("bottom_height", 320))
        self.bottom_viewer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.main_layout.addWidget(self.bottom_viewer)

        wrapper = QWidget()
        wrapper.setLayout(self.main_layout)
        self.setCentralWidget(wrapper)

        # 플로팅 버튼 구성
        self.fullscreen_button = QPushButton("전체화면", self)
        self.exit_fullscreen_button = QPushButton("일반모드", self)

        for btn in [self.fullscreen_button, self.exit_fullscreen_button]:
            btn.setFixedSize(100, 30)
            btn.setVisible(False)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(0,0,0,0);
                    color: rgba(0,0,0,0);
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgba(30,30,30,0.7);
                    color: white;
                    border: 1px solid #666;
                }
            """)
            btn.raise_()

        self.fullscreen_button.clicked.connect(self.enter_fullscreen)
        self.exit_fullscreen_button.clicked.connect(self.exit_fullscreen)

        # 마우스 위치 감지 타이머
        self.mouse_timer = QTimer()
        self.mouse_timer.timeout.connect(self.check_mouse_position)
        self.mouse_timer.start(100)

        # 자동 전체화면 진입
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.check_monitor_change)
        self.monitor_timer.start(1000)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        y = self.header.height() + 20
        x = self.width() - 120
        self.fullscreen_button.move(x, y)
        self.exit_fullscreen_button.move(x, y)

    def check_mouse_position(self):
        """
        마우스 위치에 따라 버튼 표시 조건 처리
        """
        cursor = self.mapFromGlobal(self.cursor().pos())
        btn_area = self.fullscreen_button.geometry()
        header_area = self.header.geometry()

        if self.is_fullscreen:
            if header_area.contains(cursor) or btn_area.contains(cursor):
                self.exit_fullscreen_button.setVisible(True)
            else:
                self.exit_fullscreen_button.setVisible(False)
        else:
            self.fullscreen_button.setVisible(True)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape and self.is_fullscreen:
            self.exit_fullscreen()

    def enter_fullscreen(self):
        self.showFullScreen()
        QTimer.singleShot(200, self._after_fullscreen)

    def _after_fullscreen(self):
        self.is_fullscreen = True
        self.fullscreen_button.setVisible(False)
        self.exit_fullscreen_button.setVisible(False)
        self.bottom_viewer.set_fullscreen(True)

    def exit_fullscreen(self):
        self.showNormal()
        QTimer.singleShot(200, self._after_exit_fullscreen)

    def _after_exit_fullscreen(self):
        self.is_fullscreen = False
        self.exit_fullscreen_button.setVisible(False)
        self.fullscreen_button.setVisible(True)
        self.bottom_viewer.set_fullscreen(False)

    def check_monitor_change(self):
        screens = QApplication.screens()
        if len(screens) > 1 and self.current_screen_index != 1:
            geo = screens[1].geometry()
            self.move(geo.x(), geo.y())
            self.resize(geo.width(), geo.height())
            self.enter_fullscreen()
            self.current_screen_index = 1
