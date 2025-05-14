# PPS_Player/core/media_viewer.py
# ---------------------------
# Version History
# v0.0.5 - 2025.04.26 - gif 재생 (QMovie) 및 mp4 보강 처리
# ---------------------------

from PyQt5.QtWidgets import QLabel, QStackedLayout, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QPixmap, QMovie
import os

class MediaViewer(QWidget):
    def __init__(self, media_paths, interval=5000, rolling=True):
        super().__init__()
        self.media_paths = media_paths
        self.interval = interval
        self.rolling = rolling
        self.current_index = 0
        self.is_fullscreen = False

        self.image_label = QLabel("[이미지 로딩 실패]")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: black;")
        self.movie = None  # QMovie 인스턴스 보관용

        self.video_widget = QVideoWidget()
        self.video_player = QMediaPlayer()
        self.video_player.setVideoOutput(self.video_widget)
        self.video_player.mediaStatusChanged.connect(self.on_video_status_changed)

        self.stack = QStackedLayout()
        self.stack.addWidget(self.image_label)
        self.stack.addWidget(self.video_widget)
        self.setLayout(self.stack)

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_media)

        if self.rolling:
            self.timer.start(self.interval)

        self.show_media()

    def set_fullscreen(self, is_fullscreen):
        self.is_fullscreen = is_fullscreen
        self.show_media()

    def resizeEvent(self, event):
        super().resizeEvent(event)
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

        if path.lower().endswith((".jpg", ".png")):
            pixmap = QPixmap(path)
            if pixmap.isNull():
                print(f"[❌ QPixmap 로딩 실패] {path}")
                self.image_label.setText(f"[로딩 실패] {os.path.basename(path)}")
            else:
                scale_factor = 1.0 if self.is_fullscreen else 0.9
                scaled_pixmap = pixmap.scaled(self.size() * scale_factor, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)
            self.stack.setCurrentWidget(self.image_label)
            if self.rolling:
                self.timer.start(self.interval)
        elif path.lower().endswith(".gif"):
            if self.movie:
                self.movie.stop()
            self.movie = QMovie(path)
            self.image_label.setMovie(self.movie)
            self.movie.start()
            self.stack.setCurrentWidget(self.image_label)
            if self.rolling:
                self.timer.start(self.interval)
        elif path.lower().endswith(".mp4"):
            self.video_player.stop()
            self.video_player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
            self.stack.setCurrentWidget(self.video_widget)
            self.video_player.play()
            self.timer.stop()

    def on_video_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.next_media()

    def next_media(self):
        self.current_index = (self.current_index + 1) % len(self.media_paths)
        self.show_media()
