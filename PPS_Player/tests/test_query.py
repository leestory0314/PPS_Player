import sys
from pathlib import Path

# 프로젝트 루트의 부모 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.database import get_connection

def inspect_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM table_status ORDER BY timestamp DESC LIMIT 5")
        rows = cursor.fetchall()
        if not rows:
            print("⚠️  데이터가 없습니다.")
        else:
            print(f"✅ {len(rows)}개 데이터 조회됨:")
            for row in rows:
                print(row)

if __name__ == "__main__":
    inspect_table()
