import sys
import subprocess
import re
from pathlib import Path

VERSION_FILE = Path(__file__).parent / ".version"

def read_version():
    if not VERSION_FILE.exists():
        print("⚠️ .version 파일이 존재하지 않습니다. 먼저 생성해주세요.")
        sys.exit(1)
    return VERSION_FILE.read_text(encoding="utf-8").strip()

def write_version(new_version: str):
    VERSION_FILE.write_text(new_version, encoding="utf-8")



def bump_version(current_version: str, level: str) -> str:
    match = re.match(r'v(\d+)\.(\d+)\.(\d+)', current_version)
    if not match:
        raise ValueError("버전 형식이 잘못되었습니다. vX.X.X 형식이어야 합니다.")

    major, minor, patch = map(int, match.groups())

    if level == 'patch':
        patch += 1
    elif level == 'minor':
        minor += 1
        patch = 0
    elif level == 'major':
        major += 1
        minor = 0
        patch = 0
    else:
        raise ValueError("증분 단위는 patch, minor, major 중 하나여야 합니다.")

    return f"v{major}.{minor}.{patch}"

def git_commit_and_tag(version: str, message: str):
    subprocess.run(["git", "add", ".version"], check=True)
    subprocess.run(["git", "commit", "-m", f"[version] Bump to {version}: {message}"], check=True)
    subprocess.run(["git", "tag", version, "-m", message], check=True)
    subprocess.run(["git", "push"], check=True)
    subprocess.run(["git", "push", "origin", version], check=True)

def main():
    if len(sys.argv) < 3:
        print("❗ 사용법: python version_bump.py [patch|minor|major] '커밋 메시지'")
        sys.exit(1)

    level = sys.argv[1]
    message = sys.argv[2]

    current = read_version()
    new_version = bump_version(current, level)
    write_version(new_version)

    print(f"✅ 버전 증가: {current} → {new_version}")
    git_commit_and_tag(new_version, message)

if __name__ == "__main__":
    main()
