# PPS_Player/core/voice_manager.py
# ---------------------------
# Version History
# v0.0.1 - 2025.04.25 - 음성 수신 및 자막 출력 구조 설계 시작
# ---------------------------

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QUrl, QTimer

class VoiceManager:
    def __init__(self, subtitle_label: QLabel):
        self.player = QMediaPlayer()
        self.subtitle_label = subtitle_label

    def play_voice(self, filepath, subtitle_text):
        self.subtitle_label.setText(subtitle_text)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(filepath)))
        self.player.play()

        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self.subtitle_label.setText(""))
        timer.start(5000)
