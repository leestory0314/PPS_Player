# ---------------------------------------
# Module: media_viewer.py
# 위치: PPS_Player/core/
# 작성 목적: 이미지/비디오 재생 UI (롤링 지원)
# ---------------------------------------
# Version History
# v0.0.3 - 2025.04.26 - rolling 인자 추가, 롤링 설정 가능하도록 수정
# v0.1.0 - 2025.05.15 - PyQt6 호환 버전으로 변환
# v0.2.0 - 2025.05.20 - 스케일 개선, 구조 리팩토링
# v0.2.1 - 2025.05.21 - 이미지 크기 개선, 구조 유틸화, 타입 힌트 추가
# ---------------------------------------

import os
from PyQt6.QtWidgets import QLabel, QStackedLayout, QWidget
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import Qt, QTimer, QUrl, QSize
from PyQt6.QtGui import QPixmap


class MediaViewer(QWidget):
    def __init__(self, media_paths: list[str], interval: int = 5000, rolling: bool = True):
        super().__init__()
        self.media_paths = media_paths or []
        self.interval = interval
        self.rolling = rolling
        self.current_index = 0

        # 이미지 출력용
        self.image_label = QLabel("🔇 표시할 미디어가 없습니다.")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: black; color: gray; font-size: 16px;")

        # 비디오 출력용
        self.video_widget = QVideoWidget()
        self.video_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.video_player.setAudioOutput(self.audio_output)
        self.video_player.setVideoOutput(self.video_widget)
        self.video_player.mediaStatusChanged.connect(self.on_video_status_changed)

        # 스택 레이아웃 구성
        self.stack = QStackedLayout()
        self.stack.addWidget(self.image_label)
        self.stack.addWidget(self.video_widget)
        self.setLayout(self.stack)

        # 타이머
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_media)

        # 초기 미디어 로드
        if self.media_paths:
            self.show_media()
            if self.rolling:
                self.timer.start(self.interval)

    def show_media(self):
        if not self.media_paths:
            self.set_error_message("🔇 표시할 미디어가 없습니다.")
            return

        path = os.path.abspath(self.media_paths[self.current_index])
        print(f"[MediaViewer] 미디어 로딩 시도: {path}")

        if not os.path.exists(path):
            self.set_error_message(f"[파일 없음] {os.path.basename(path)}")
            return

        ext = os.path.splitext(path)[1].lower()
        if ext in [".jpg", ".jpeg", ".png", ".gif"]:
            self.load_image(path)
        elif ext in [".mp4", ".avi", ".webm"]:
            self.load_video(path)
        else:
            self.set_error_message("❌ 지원되지 않는 형식")

    def load_image(self, path: str):
        pixmap = QPixmap(path)
        if pixmap.isNull():
            print(f"[MediaViewer] ❌ QPixmap 로딩 실패: {path}")
            self.set_error_message(f"[로딩 실패] {os.path.basename(path)}")
            return

        scaled = pixmap.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled)
        self.stack.setCurrentWidget(self.image_label)
        self.video_player.stop()

    def load_video(self, path: str):
        self.video_player.setSource(QUrl.fromLocalFile(path))
        self.stack.setCurrentWidget(self.video_widget)
        self.video_player.play()

    def on_video_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.next_media()

    def next_media(self):
        if not self.media_paths:
            return
        self.current_index = (self.current_index + 1) % len(self.media_paths)
        self.show_media()

    def set_error_message(self, message: str):
        self.image_label.setText(message)
        self.stack.setCurrentWidget(self.image_label)
        self.video_player.stop()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 화면 크기 변화 시 이미지 다시 스케일링
        if self.stack.currentWidget() == self.image_label and self.media_paths:
            self.show_media()

    def set_fullscreen(self, is_full: bool):
        # 향후 전체화면 대응용
        pass
