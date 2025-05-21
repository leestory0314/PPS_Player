# PPS_Player/core/database.py

import sqlite3

def migrate_db(db_path="local.sqlite"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS store_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_uid TEXT,
        brand_name TEXT,
        store_name TEXT,
        contact TEXT,
        logo_url TEXT
    )
    """)
    # 추후 media_queue, config 등도 여기에 추가 가능

    conn.commit()
    conn.close()
