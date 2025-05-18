# core/dashboard_scraper.py
# Version History
# v0.2.6 - config 기반 store_idx/z_idx 통합 및 run_scraper 포함

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

from core.database import insert_table_status
from config.config_loader import (
    get_store_id, get_store_pw, get_store_zone_id,
    get_store_idx, get_store_z_idx
)

def login_and_get_session():
    """로그인 후 세션 반환"""
    store_id = get_store_id()
    store_pw = get_store_pw()
    store_zone = get_store_zone_id()
    store_id_chk = "1"

    session = requests.Session()

    # 사전 store_id 유효성 확인 (선택적)
    zone_url = f"https://taggugo.kr/dashboard/proc/store_zone_options.php?store_id={store_id}"
    try:
        session.get(zone_url, timeout=3)
    except:
        pass  # 무시하고 진행

    login_url = "https://taggugo.kr/dashboard/proc/proc_store_login.php"
    login_payload = {
        "store_id": store_id,
        "store_pw": store_pw,
        "store_id_chk": store_id_chk,
        "store_zone": store_zone
    }
    login_resp = session.post(login_url, data=login_payload)

    if "location.replace" in login_resp.text or login_resp.ok:
        print("✅ 로그인 성공")
        return session
    else:
        print("❌ 로그인 실패")
        return None

def fetch_dashboard_html(session):
    """대시보드 API 요청 후 HTML 반환"""
    store_idx = get_store_idx()
    store_z_idx = get_store_z_idx()
    print(f"📌 store_idx: {store_idx}, store_z_idx: {store_z_idx}")

    api_url = "https://taggugo.kr/dashboard/proc/ajax_use_state_audio.php"
    resp = session.post(api_url, data={"store_idx": store_idx, "store_z_idx": store_z_idx})

    if resp.ok:
        data = resp.json()
        html = data.get("return_html", "")
        print("📥 응답 HTML 미리보기:")
        print(html[:300])
        return html
    else:
        print("❌ 대시보드 API 호출 실패")
        return ""

def parse_dashboard_html(html: str, store_id: str):
    """HTML 파싱 및 DB 저장"""
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select('div.tr-fx-nw.tr-fxstr.tr-fx-c.p-20-c')

    print(f"📦 파싱된 카드 수: {len(cards)}")
    now = datetime.now()

    for card in cards:
        try:
            table_name = card.select_one(".bold").get_text(strip=True)
            spans = card.select("span")
            user_name = spans[1].get_text(strip=True)
            start_str = spans[3].get_text(strip=True)
            end_str = spans[5].get_text(strip=True)

            start_dt = datetime.strptime(f"{now.year}.{start_str}", "%Y.%m.%d %H:%M")
            end_dt = datetime.strptime(f"{now.year}.{end_str}", "%Y.%m.%d %H:%M")
            remaining = int((end_dt - now).total_seconds())

            status = "playing"
            if remaining <= 0:
                status = "ended"
            elif remaining < 300:
                status = "ending_soon"

            insert_table_status({
                "store_id": store_id,
                "table_name": table_name,
                "user_name": user_name,
                "start_time": start_dt.isoformat(),
                "end_time": end_dt.isoformat(),
                "remaining_time": remaining,
                "status": status
            })

            print(f"✅ 저장: {table_name} / {user_name} / {status}")
        except Exception as e:
            logging.warning(f"[ParseError] {e} / Card: {card}")

def run_scraper():
    """외부에서 호출 가능한 실행 진입점"""
    session = login_and_get_session()
    if not session:
        return

    html = fetch_dashboard_html(session)
    if html:
        parse_dashboard_html(html, get_store_id())
