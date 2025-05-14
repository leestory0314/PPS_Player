# PPS_Player/utils/utils.py
# ---------------------------
# Version History
# v0.0.1 - 2025.04.25 - 최초 작성: 파일 존재 확인 유틸리티 추가 예정
# ---------------------------

import os

def file_exists(path):
    return os.path.isfile(path)