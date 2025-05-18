import sys
from pathlib import Path
import requests  # ✅ 반드시 이 줄이 있어야 합니다!

# PYTHONPATH 설정 (core/ → config/ 접근 가능하게)
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.config_loader import get_store_idx, get_store_z_idx

# 1. 로그인 정보 설정
store_id = "ppstation"
store_pw = "ppstation"
store_zone = "안산고잔점"
store_id_chk = "1"

# 2. 세션 객체 생성
session = requests.Session()

# 3. 사전 인증 요청 (store_id 확인)
zone_url = f"https://taggugo.kr/dashboard/proc/store_zone_options.php?store_id={store_id}"
zone_resp = session.get(zone_url)
if not zone_resp.ok or not zone_resp.text.strip():
    print("❌ 유효하지 않은 store_id 입니다.")
    exit()

# 4. 로그인 요청
login_url = "https://taggugo.kr/dashboard/proc/proc_store_login.php"
login_payload = {
    "store_id": store_id,
    "store_pw": store_pw,
    "store_id_chk": store_id_chk,
    "store_zone": store_zone
}
login_resp = session.post(login_url, data=login_payload)

# 5. 로그인 성공 판단
if "location.replace" in login_resp.text or login_resp.ok:
    print("✅ 로그인 성공")

    # 6. config에서 store_idx 정보 불러오기
    store_idx = get_store_idx()
    store_z_idx = get_store_z_idx()
    print(f"📌 store_idx: {store_idx}, store_z_idx: {store_z_idx}")

    # 7. 대시보드 API 호출 (로그인된 세션으로)
    dashboard_url = "https://taggugo.kr/dashboard/proc/ajax_use_state_audio.php"
    api_resp = session.post(dashboard_url, data={
        "store_idx": store_idx,
        "store_z_idx": store_z_idx
    })

    if api_resp.ok:
        data = api_resp.json()
        html = data.get("return_html", "")
        print("📥 로그인 후 응답 HTML:")
        print(html[:500])
    else:
        print("❌ API 호출 실패", api_resp.status_code)
else:
    print("❌ 로그인 실패. 응답 내용:")
    print(login_resp.text)
