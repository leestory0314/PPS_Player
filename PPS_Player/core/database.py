# core/database.py
# Version History
# v0.2.1 - table_status 테이블 생성 및 insert 함수 구현

import sqlite3
from pathlib import Path

# DB 파일 경로 설정 (최상위 디렉토리에 store_data.db 생성)
DB_PATH = Path(__file__).parent.parent / "store_data.db"

def get_connection():
    """SQLite DB 연결 반환"""
    return sqlite3.connect(DB_PATH)

def init_db():
    """table_status 테이블이 없으면 생성"""
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS table_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id TEXT,
            table_name TEXT,
            user_name TEXT,
            start_time TEXT,
            end_time TEXT,
            remaining_time INTEGER,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

def insert_table_status(data: dict):
    """table_status 테이블에 한 건 삽입"""
    with get_connection() as conn:
        conn.execute("""
        INSERT INTO table_status (
            store_id, table_name, user_name,
            start_time, end_time, remaining_time, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data["store_id"],
            data["table_name"],
            data["user_name"],
            data["start_time"],
            data["end_time"],
            data["remaining_time"],
            data["status"]
        ))
        conn.commit()
