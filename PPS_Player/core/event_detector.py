# core/event_detector.py
# Version History
# v0.2.8 - 테이블 상태 변화 감지 + TTS 발음 최적화 통합

from core.database import get_connection
from core.tts_manager import speak
from datetime import datetime


def normalize_table_name(table_name: str) -> str:
    """TTS 자연스러운 발음을 위해 숫자를 한글로 변환"""
    num_map = {
        "1": "일", "2": "이", "3": "삼", "4": "사", "5": "오",
        "6": "육", "7": "칠", "8": "팔", "9": "구", "10": "십"
    }

    for num, kor in num_map.items():
        if table_name.startswith(f"{num}번"):
            table_name = table_name.replace(f"{num}번", f"{kor}번", 1)
            break
    return table_name


def fetch_latest_status():
    """현재 테이블의 최신 상태 목록 가져오기"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name, user_name, status, MAX(timestamp)
            FROM table_status
            GROUP BY table_name
        """)
        return cursor.fetchall()


def detect_events(previous, current):
    """이전 상태와 비교해 변화된 이벤트 추출"""
    events = []
    for table_name, curr in current.items():
        prev = previous.get(table_name)
        if not prev:
            events.append((table_name, "started", curr))
        elif prev["status"] != curr["status"]:
            if curr["status"] == "ending_soon":
                events.append((table_name, "ending_soon", curr))
            elif curr["status"] == "ended":
                events.append((table_name, "ended", curr))
    return events


def run_event_detector():
    """상태 변화 감지 및 트리거 처리"""
    current_state = {}

    # 1. DB에서 최신 상태 전체 조회
    rows = fetch_latest_status()
    new_state = {}
    for row in rows:
        table_name, user_name, status, _ = row
        new_state[table_name] = {
            "user_name": user_name,
            "status": status
        }

    # 2. 상태 변화 감지
    events = detect_events(current_state, new_state)

    # 3. 이벤트에 따른 TTS 출력
    for table_name, event_type, info in events:
        spoken_name = normalize_table_name(table_name)

        if event_type == "started":
            print(f"🟢 {table_name} 게임 시작 감지 - {info['user_name']}")
            speak(f"{spoken_name} 게임이 시작되었습니다")

        elif event_type == "ending_soon":
            print(f"🟡 {table_name} 종료 임박 감지")
            speak(f"{spoken_name} 5분 남았습니다")

        elif event_type == "ended":
            print(f"🔴 {table_name} 게임 종료 감지")
            speak(f"{spoken_name} 게임이 종료되었습니다")

    return new_state  # 현재 상태 반환 (다음 루프 등 활용 가능)
