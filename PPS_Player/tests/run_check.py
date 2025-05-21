# run_check.py (또는 임시로 app.py에 추가)

import sqlite3

conn = sqlite3.connect("local.sqlite")
cursor = conn.cursor()

cursor.execute("SELECT * FROM store_info")
rows = cursor.fetchall()

print("✅ store_info 데이터:", rows)

conn.close()
