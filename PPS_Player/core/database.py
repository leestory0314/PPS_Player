# core/database.py

import sqlite3

DB_PATH = "store_data.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
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
