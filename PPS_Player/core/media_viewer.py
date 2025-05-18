# PPS_Player/core/media_viewer.py
# ---------------------------
# Version History
# v0.0.3 - 2025.04.26 - rolling 인자 추가, 롤링 설정 가능하도록 수정
# v0.1.0 - 2025.05.15 - PyQt6 호환 버전으로 변환
# ---------------------------

from PyQt6.QtWidgets import QLabel, QStackedLayout, QWidget
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QPixmap
import os

class MediaViewer(QWidget):
    def __init__(self, media_paths, interval=5000, rolling=True):
        super().__init__()
        self.media_paths = media_paths
        self.interval = interval
        self.rolling = rolling
        self.current_index = 0

        # 이미지 표시용
        self.image_label = QLabel("[이미지 로딩 실패]")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: black;")

        # 비디오 표시용
        self.video_widget = QVideoWidget()
        self.video_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.video_player.setAudioOutput(self.audio_output)
        self.video_player.setVideoOutput(self.video_widget)
        self.video_player.mediaStatusChanged.connect(self.on_video_status_changed)

        # 스택 레이아웃으로 이미지/비디오 전환
        self.stack = QStackedLayout()
        self.stack.addWidget(self.image_label)
        self.stack.addWidget(self.video_widget)
        self.setLayout(self.stack)

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_media)

        if self.rolling:
            self.timer.start(self.interval)

        self.show_media()

    def show_media(self):
        if not self.media_paths:
            self.image_label.setText("[재생할 미디어 없음]")
            self.stack.setCurrentWidget(self.image_label)
            return

        path = self.media_paths[self.current_index]
        print(f"[미디어 경로] {path}")
        if not os.path.exists(path):
            print(f"[❌ 경로 존재 안함] {os.path.abspath(path)}")
            self.image_label.setText(f"[파일 없음] {os.path.basename(path)}")
            self.stack.setCurrentWidget(self.image_label)
            if self.rolling:
                self.timer.start(self.interval)
            return

        if path.lower().endswith((".jpg", ".png", ".gif")):
            pixmap = QPixmap(path)
            if pixmap.isNull():
                print(f"[❌ QPixmap 로딩 실패] {path}")
                self.image_label.setText(f"[로딩 실패] {os.path.basename(path)}")
            else:
                self.image_label.setPixmap(pixmap.scaled(
                    self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.stack.setCurrentWidget(self.image_label)
            if self.rolling:
                self.timer.start(self.interval)
        elif path.lower().endswith(".mp4"):
            self.video_player.setSource(QUrl.fromLocalFile(path))
            self.stack.setCurrentWidget(self.video_widget)
            self.video_player.play()
            self.timer.stop()

    def on_video_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.next_media()

    def next_media(self):
        self.current_index = (self.current_index + 1) % len(self.media_paths)
        self.show_media()

    def set_fullscreen(self, is_full):
        # UI 모드 대응을 위한 placeholder
        pass
