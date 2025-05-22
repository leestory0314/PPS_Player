# ---------------------------------------
# Module: media_viewer.py
# 위치: PPS_Player/core/
# 목적: 이미지 / GIF / 동영상 하단 재생 위젯
# ---------------------------------------
# Version History
# v0.3.4 - 2025.05.22 - GIF 초기 사이즈 문제 해결 (지연 실행)
# ---------------------------------------

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QUrl, QSize
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtGui import QMovie, QPixmap
import os


class MediaViewer(QWidget):
    def __init__(self, media_paths, rolling=False, debug=False, parent=None):
        super().__init__(parent)
        self.media_paths = media_paths
        self.rolling = rolling
        self.debug = debug
        self.current_index = 0

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

        self.video_widget = QVideoWidget()
        self.layout.addWidget(self.video_widget)
        self.video_widget.hide()

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_media)

        if self.debug:
            self.setStyleSheet("border: 1px solid #ff4444;")

        self.start()

    def start(self):
        if not self.media_paths:
            return
        self.show_media(self.media_paths[0])
        if self.rolling:
            self.timer.start(10000)

    def next_media(self):
        self.current_index = (self.current_index + 1) % len(self.media_paths)
        self.show_media(self.media_paths[self.current_index])

    def show_media(self, path):
        ext = os.path.splitext(path)[-1].lower()
        if ext == ".gif":
            self.video_widget.hide()
            self.label.show()
            movie = QMovie(path)
            self.label.setMovie(movie)

            def delayed_start():
                movie.setScaledSize(self.size())
                movie.start()

            QTimer.singleShot(200, delayed_start)
        elif ext == ".mp4":
            self.label.hide()
            self.video_widget.show()
            self.player.setSource(QUrl.fromLocalFile(path))
            self.player.play()
        else:
            self.video_widget.hide()
            self.label.show()
            self.label.setPixmap(QPixmap(path).scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.label.movie():
            self.label.movie().setScaledSize(self.size())

    def set_fullscreen(self, enabled: bool):
        pass
