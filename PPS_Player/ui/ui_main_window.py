# PPS_Player/ui/ui_main_window.py
# ---------------------------
# Version History
# v0.3.5 - 2025.05.15 - PyQt6 전환 후 consoleMessage 대응 (QWebEnginePage 서브클래스)
# ---------------------------

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWebEngineCore import QWebEngineScript
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication, QHBoxLayout, QMessageBox
from PPS_Player.core.media_viewer import MediaViewer
import pyttsx3

class CustomWebPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        if msg.startswith("TTS:"):
            text = msg[4:].strip()
            print(f"🔊 TTS 감지: {text}")
            if self.parent() and hasattr(self.parent(), "tts_engine"):
                self.parent().tts_engine.say(text)
                self.parent().tts_engine.runAndWait()

class MainWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.is_fullscreen = False
        self.current_screen_index = 0
        self.tts_engine = pyttsx3.init()
        self.init_ui()

    def init_ui(self):
        self.resize(1024, 768)
        self.setWindowTitle("PPS 플레이어")

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.center_view = QWebEngineView()
        self.center_page = CustomWebPage(self.center_view)
        self.center_view.setPage(self.center_page)
        self.preload_tts_patch()

        url = self.config.get("url", "https://www.example.com")
        self.center_view.load(QUrl(url))

        refresh_interval = max(self.config.get("web_refresh_interval", 10000), 5000)
        self.web_refresh_timer = QTimer()
        self.web_refresh_timer.timeout.connect(
            lambda: self.center_view.page().runJavaScript("if (typeof dashboard_update === 'function') dashboard_update();")
        )
        self.web_refresh_timer.start(refresh_interval)

        media_paths = self.config.get("media_paths", [])
        media_rolling = self.config.get("media_rolling", True)
        bottom_height = self.config.get("bottom_height", 300)

        self.bottom_viewer = MediaViewer(media_paths, rolling=media_rolling)
        self.bottom_viewer.setFixedHeight(bottom_height)

        self.test_button = QPushButton("🔊 테스트 음성 출력", self)
        self.test_button.setFixedSize(160, 30)
        self.test_button.clicked.connect(self.test_tts_console_injection)

        self.fullscreen_button = QPushButton("전체화면", self)
        self.fullscreen_button.setFixedSize(120, 30)
        self.fullscreen_button.clicked.connect(self.enter_fullscreen)

        self.exit_fullscreen_button = QPushButton("일반모드", self)
        self.exit_fullscreen_button.setFixedSize(120, 30)
        self.exit_fullscreen_button.clicked.connect(self.exit_fullscreen)
        self.exit_fullscreen_button.hide()

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.test_button)
        self.button_layout.addWidget(self.fullscreen_button)
        self.button_layout.addWidget(self.exit_fullscreen_button)

        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.center_view)
        self.main_layout.addWidget(self.bottom_viewer)
        self.setLayout(self.main_layout)

        self.mouse_timer = QTimer()
        self.mouse_timer.timeout.connect(self.check_mouse_position)
        self.mouse_timer.start(100)

        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.check_monitor_change)
        self.monitor_timer.start(1000)

    def preload_tts_patch(self):
        patch_js = '''
        (function() {
          function patchTTS() {
            if (typeof window.speechSynthesis === "undefined") {
              window.speechSynthesis = {
                speak: function(u) {
                  if (u && u.text) console.log("TTS:" + u.text);
                }
              };
            }
            if (typeof SpeechSynthesisUtterance === "undefined") {
              window.SpeechSynthesisUtterance = function(text) {
                console.log("TTS:" + text);
                return { text: text };
              };
            }
            console.log("✅ speech patch injected");
          }
          patchTTS();
          const observer = new MutationObserver(() => patchTTS());
          observer.observe(document.body, { childList: true, subtree: true });
        })();
        '''
        script = QWebEngineScript()
        script.setName("TTSInject")
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentReady)
        script.setRunsOnSubFrames(True)
        script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        script.setSourceCode(patch_js)
        self.center_view.page().profile().scripts().insert(script)

    def test_tts_console_injection(self):
        try:
            script = """
            if (typeof SpeechSynthesisUtterance !== 'undefined') {
                var u = new SpeechSynthesisUtterance("테스트 음성 출력입니다");
                speechSynthesis.speak(u);
            } else {
                console.log("TTS:테스트 음성 출력입니다");
            }
            """
            self.center_view.page().runJavaScript(script)
        except Exception as e:
            QMessageBox.warning(self, "TTS 테스트 실패", f"자바스크립트 실행 중 오류 발생:\n{str(e)}")

    def cleanup_web_cache(self):
        pass

    def update_button_position(self):
        pass

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_button_position()

    def enter_fullscreen(self):
        self.showFullScreen()
        self.is_fullscreen = True
        self.fullscreen_button.hide()
        self.exit_fullscreen_button.hide()
        self.bottom_viewer.set_fullscreen(True)

    def exit_fullscreen(self):
        self.showNormal()
        self.is_fullscreen = False
        self.fullscreen_button.show()
        self.exit_fullscreen_button.hide()
        self.bottom_viewer.set_fullscreen(False)

    def check_mouse_position(self):
        if self.is_fullscreen:
            cursor_y = self.mapFromGlobal(self.cursor().pos()).y()
            if cursor_y < 60:
                self.exit_fullscreen_button.show()
            else:
                self.exit_fullscreen_button.hide()
        else:
            self.exit_fullscreen_button.hide()
            self.fullscreen_button.show()

    def check_monitor_change(self):
        screens = QApplication.screens()
        if len(screens) > 1:
            second = screens[1]
            if self.current_screen_index != 1:
                geo = second.geometry()
                print("🖥️ 2번 모니터 감지됨. 전체화면 전환 중...")
                self.move(geo.x(), geo.y())
                self.resize(geo.width(), geo.height())
                self.enter_fullscreen()
                self.current_screen_index = 1
        else:
            primary = QApplication.primaryScreen()
            if self.current_screen_index != 0:
                geo = primary.geometry()
                print("⬅️ 2번 모니터 사라짐. 1번으로 복귀...")
                self.showNormal()
                self.move(geo.x(), geo.y())
                self.resize(1024, 768)
                self.exit_fullscreen()
                self.raise_()
                self.activateWindow()
                self.current_screen_index = 0
