# core/tts_manager.py
# Version History
# v0.2.8 - pyttsx3 기반 음성 출력 모듈

import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 155)  # 말하는 속도 조절

def speak(text: str):
    print(f"🔊 [TTS] {text}")
    engine.say(text)
    engine.runAndWait()
