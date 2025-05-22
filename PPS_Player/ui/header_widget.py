# Version: v1.3.3 - height, font 사이즈 config 적용 보장

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import QTimer, Qt
from datetime import datetime
import os


class HeaderWidget(QWidget):
    def __init__(self, config: dict, parent=None):
        super().__init__(parent)
        self.config = config
        self._init_ui()
        self._init_timer()

    def _init_ui(self):
        height = self.config.get("header_height", 40)
        bg_color = self.config.get("header_bg_color", "#111111")
        text_color = self.config.get("header_text_color", "#ffffff")
        font_family = self.config.get("header_font", "Noto Sans KR")
        font_size = self.config.get("header_font_size", 14)

        self.setFixedHeight(height)  # 명확히 고정
        self.setStyleSheet(f"background-color: {bg_color};")

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(20)

        logo_path = self.config.get("header_logo_path", "")
        logo_label = QLabel()
        if logo_path and os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            logo_label.setPixmap(pixmap.scaledToHeight(height - 8, Qt.TransformationMode.SmoothTransformation))
        logo_label.setStyleSheet(f"background-color: {bg_color};")
        layout.addWidget(logo_label)

        message_text = self.config.get("header_message_text", "")
        self.message_label = QLabel(message_text)
        self.message_label.setFont(QFont(font_family, font_size))
        self.message_label.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.message_label, stretch=1)

        self.time_label = QLabel()
        self.time_label.setFont(QFont("Consolas", font_size))
        self.time_label.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
        layout.addWidget(self.time_label)

        self.setLayout(layout)
        self._update_time()

    def _init_timer(self):
        self.timer = QTimer(self)
        self.timer.setInterval(60000)
        self.timer.timeout.connect(self._update_time)
        self.timer.start()

    def _update_time(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.time_label.setText(now)
