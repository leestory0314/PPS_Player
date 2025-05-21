# PPS_Player/PPS_Player/tests/test_event.py

import sys
from pathlib import Path

# 상위 프로젝트 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.event_detector import run_event_detector

if __name__ == "__main__":
    state = run_event_detector()
    print("📦 현재 상태 Snapshot:")
    for table, info in state.items():
        print(f"{table}: {info['user_name']} / {info['status']}")
