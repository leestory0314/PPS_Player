import sys
from pathlib import Path

# 프로젝트 루트 패키지 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.dashboard_scraper import run_scraper
from core.database import init_db

init_db()
run_scraper()
