# PPS_Player/core/network_client.py
# ---------------------------
# Version History
# v0.0.1 - 2025.04.25 - 서버 폴링 구조 및 명령 수신 구조 설계 시작
# ---------------------------

import requests
from threading import Timer

class NetworkClient:
    def __init__(self, server_url, store_id, interval=5):
        self.server_url = server_url
        self.store_id = store_id
        self.interval = interval
        self.timer = None

    def start_polling(self, callback):
        def poll():
            try:
                resp = requests.get(f"{self.server_url}/commands/{self.store_id}")
                if resp.status_code == 200:
                    callback(resp.json())
            except Exception as e:
                print("Polling error:", e)
            self.schedule_next()

        self.schedule_next = lambda: Timer(self.interval, poll).start()
        poll()
