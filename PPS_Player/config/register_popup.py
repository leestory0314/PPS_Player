# ---------------------------------------
# Module: register_popup.py
# 위치: PPS_Player/config/
# 작성 목적: 지점 등록용 팝업 UI 및 store_info 저장
# ---------------------------------------
# Version History
# v0.1.0 - 2025.05.01 - 기본 등록 UI 및 DB 저장 구현
# v0.2.0 - 2025.05.20 - 절대경로 DB 연동 + 스타일 개선 + 구조 리팩토링
# ---------------------------------------

import os
import sqlite3
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PPS_Player.core.constants import DB_PATH


class RegisterPopup(QDialog):
    """지점 고유코드 + 인증코드를 받아 store_info 저장하는 팝업"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("지점 등록")
        self.setFixedSize(360, 260)
        self.db_path = DB_PATH
        self.setStyleSheet(self._get_stylesheet())

        font = QFont("Malgun Gothic", 10)

        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(30, 30, 30, 30)

        # 고유 코드 입력
        self.uid_input = QLineEdit()
        self.uid_input.setPlaceholderText("지점 고유 코드")
        self.uid_input.setFont(font)
        self.uid_input.setObjectName("Input")

        # 인증 코드 입력
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("인증 코드")
        self.token_input.setFont(font)
        self.token_input.setObjectName("Input")

        # 등록 버튼
        self.submit_btn = QPushButton("등록 요청")
        self.submit_btn.setFont(QFont("Malgun Gothic", 10, QFont.Weight.Bold))
        self.submit_btn.setObjectName("PrimaryButton")
        self.submit_btn.setMinimumHeight(36)
        self.submit_btn.clicked.connect(self.submit_registration)

        layout.addWidget(QLabel("고유 코드"))
        layout.addWidget(self.uid_input)
        layout.addWidget(QLabel("인증 코드"))
        layout.addWidget(self.token_input)
        layout.addStretch()
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

    def _get_stylesheet(self) -> str:
        return """
        QDialog {
            background-color: #f4f6f9;
        }
        QLabel {
            font-size: 13px;
            color: #333;
        }
        QLineEdit#Input {
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
            background-color: white;
        }
        QPushButton#PrimaryButton {
            background-color: #3578e5;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton#PrimaryButton:hover {
            background-color: #2c64c7;
        }
        """

    def submit_registration(self):
        uid = self.uid_input.text().strip()
        token = self.token_input.text().strip()

        if not uid or not token:
            QMessageBox.warning(self, "입력 오류", "모든 항목을 입력해주세요.")
            return

        # ✅ 서버 응답 시뮬레이션
        data = {
            "store_info": {
                "store_uid": uid,
                "brand_name": "핑퐁스테이션",
                "store_name": "테스트지점",
                "contact": "010-0000-0000",
                "logo_url": "assets/logo.png"
            }
        }

        try:
            self.save_to_db(data)
            QMessageBox.information(self, "등록 완료", "지점 등록이 완료되었습니다.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "DB 저장 실패", str(e))

    def save_to_db(self, data: dict):
        print("[SAVE] DB 경로:", self.db_path)

        store = data.get("store_info", {})
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM store_info")  # 항상 1개만 유지
        cursor.execute("""
            INSERT INTO store_info (store_uid, brand_name, store_name, contact, logo_url)
            VALUES (?, ?, ?, ?, ?)
        """, (
            store.get("store_uid"),
            store.get("brand_name"),
            store.get("store_name"),
            store.get("contact"),
            store.get("logo_url")
        ))

        conn.commit()
        conn.close()
        print("✅ store_info 저장됨:", store.get("store_uid"))
