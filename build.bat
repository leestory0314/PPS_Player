@echo off
echo [🛠 PPS_Player 빌드 시작]

REM 경로 초기화
cd /d %~dp0

REM PyInstaller 실행 (최적화 포함)
pyinstaller PPS_Player/app.py ^
  --noconfirm ^
  --clean ^
  --name PPS_Player ^
  --windowed ^
  --exclude-module PyQt5.QtWebKit ^
  --exclude-module tests ^
  --add-data "config.json;." ^
  --add-data "resources;resources"

echo [✅ 빌드 완료] dist\PPS_Player\PPS_Player.exe 생성됨
pause
