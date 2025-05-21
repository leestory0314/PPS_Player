from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import QTimer, QDateTime, Qt
import sqlite3

class HeaderWidget(QWidget):
    def __init__(self, db_path: str, height: int = 30):  # ✅ height 인자 추가
        super().__init__()
        self.db_path = db_path

        self.logo_label = QLabel()
        self.info_label = QLabel()
        self.time_label = QLabel()

        self._setup_ui()
        self._load_store_info()
        self._start_clock()
        self.setFixedHeight(height)  # ✅ 설정된 높이 적용

    def _setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 4, 15, 4)  # ✅ 마진 축소

        self.logo_label.setFixedSize(32, 32)  # ✅ 로고 크기 고정

        self.info_label.setFont(QFont("Malgun Gothic", 10))  # ✅ 폰트 축소
        self.info_label.setStyleSheet("color: white;")

        self.time_label.setFont(QFont("Segoe UI", 10))  # ✅ 시계도 동일
        self.time_label.setStyleSheet("color: white;")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(self.logo_label)
        layout.addSpacing(10)
        layout.addWidget(self.info_label)
        layout.addStretch()
        layout.addWidget(self.time_label)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #222;")



    def _load_store_info(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT brand_name, store_name, contact, logo_url FROM store_info LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if row:
            brand, store, contact, logo_url = row
            self.info_label.setText(f"{brand} | {store}   {contact}")
            if logo_url and logo_url.strip():
                self.logo_label.setPixmap(QPixmap(logo_url).scaledToHeight(32))

    def _start_clock(self):
        self._update_time()
        timer = QTimer(self)
        timer.timeout.connect(self._update_time)
        timer.start(1000)

    def _update_time(self):
        now = QDateTime.currentDateTime()
        self.time_label.setText(now.toString("MM/dd HH:mm"))
