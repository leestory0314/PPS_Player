# PPS_Player/core/music_player.py
# ---------------------------
# Version History
# v0.0.1 - 2025.04.25 - 배경 음악 플레이어 구조 설계 시작
# ---------------------------

from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtCore import QUrl

class MusicPlayer:
    def __init__(self, music_paths, mode='loop'):
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        for path in music_paths:
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(path)))

        if mode == 'shuffle':
            self.playlist.setPlaybackMode(QMediaPlaylist.Random)
        elif mode == 'repeat_one':
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
        else:
            self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        self.player.setPlaylist(self.playlist)
        self.player.setVolume(100)
        self.player.play()