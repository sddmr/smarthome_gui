import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QDialog, QGridLayout, QFrame, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFont

PIN_CODE = "0000"


class NumPad(QDialog):
    """Dokunmatik numpad şifre penceresi."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Şifre Gir")
        self.setModal(True)
        self.setFixedSize(320, 420)
        self.setStyleSheet("background: #121212; color: white; border-radius: 12px;")
        self.password = ""

        v = QVBoxLayout(self)
        self.display = QLabel("Şifre: ")
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setFont(QFont("Sans", 18, QFont.Bold))
        v.addWidget(self.display)

        grid = QGridLayout()
        grid.setSpacing(8)
        btn_style = """
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #2b2b2b, stop:1 #1a1a1a);
                color: white; border-radius: 10px; font-size:18px; padding:12px;
            }
            QPushButton:pressed { background: #444; }
        """
        keys = [
            ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
            ("←", 3, 0), ("0", 3, 1), ("OK", 3, 2),
        ]
        for k, r, c in keys:
            b = QPushButton(k)
            b.setStyleSheet(btn_style)
            b.clicked.connect(self.on_key)
            grid.addWidget(b, r, c)
        v.addLayout(grid)

    def on_key(self):
        key = self.sender().text()
        if key == "←":
            self.password = self.password[:-1]
        elif key == "OK":
            if self.password == PIN_CODE:
                self.accept()
            else:
                QMessageBox.warning(self, "Hata", "Yanlış şifre!")
                self.password = ""
        else:
            if len(self.password) < 8:
                self.password += key
        self.display.setText("Şifre: " + "*" * len(self.password))


class InfoCard(QFrame):
    """Küçük bilgi kartı (başlık + içerik)."""
    def __init__(self, title: str, content: str = "", height=140):
        super().__init__()
        self.setObjectName("InfoCard")
        self.setFixedHeight(height)
        self.setStyleSheet("""
            QFrame#InfoCard {
                background: rgba(255,255,255,0.04);
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.03);
            }
            QLabel { color: white; background: transparent; }
        """)
        v = QVBoxLayout(self)
        self.title_lbl = QLabel(title)
        self.title_lbl.setFont(QFont("Sans", 12, QFont.Bold))
        self.content_lbl = QLabel(content)
        self.content_lbl.setFont(QFont("Sans", 11))
        self.content_lbl.setWordWrap(True)
        v.addWidget(self.title_lbl)
        v.addStretch(1)
        v.addWidget(self.content_lbl)


class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Akıllı Ev - Panel")
        self.showFullScreen()
        # Genel stil (gradient, modern)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                                           stop:0 #0f1113, stop:1 #1b1d20);
                color: white;
                font-family: 'Sans';
            }
        """)
        self.alarm_active = False
        self.flash_state = False
        self.init_ui()
        self.start_clock()

        # Alarm flash timer
        self.alarm_flash_timer = QTimer(self)
        self.alarm_flash_timer.timeout.connect(self.flash_alarm)

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 18, 28, 18)
        root.setSpacing(18)

        # --- TOP BAR ---
        top = QHBoxLayout()
        top.setSpacing(12)

        # left: big clock
        self.clock = QLabel()
        self.clock.setFont(QFont("Sans", 34, QFont.Bold))
        self.clock.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        top.addWidget(self.clock, stretch=1)

        # center title
        title = QLabel("AKILLI EV PANELİ")
        title.setFont(QFont("Sans", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        top.addWidget(title, stretch=1)

        # right icons
        right_icons = QHBoxLayout()
        right_icons.setSpacing(10)
        self.wifi = QLabel("📶")
        self.battery = QLabel("🔋")
        self.user = QLabel("👤")
        for w in (self.wifi, self.battery, self.user):
            w.setFont(QFont("Sans", 18))
            w.setFixedWidth(36)
            w.setAlignment(Qt.AlignCenter)
            right_icons.addWidget(w)
        top.addLayout(right_icons, stretch=1)
        root.addLayout(top)

        # --- MIDDLE GRID (2x2) ---
        grid = QGridLayout()
        grid.setSpacing(18)

        # Camera card - sol üst (placeholder siyah box)
        self.camera_card = QFrame()
        self.camera_card.setObjectName("camera_card")
        self.camera_card.setStyleSheet("""
            QFrame#camera_card {
                background: black;
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.03);
            }
        """)
        cam_layout = QVBoxLayout(self.camera_card)
        cam_title = QLabel("Kamera")
        cam_title.setFont(QFont("Sans", 12, QFont.Bold))
        cam_title.setStyleSheet("color: white; background: transparent;")
        cam_preview = QLabel("• Kamera görüntüsü buraya gelecek •")
        cam_preview.setAlignment(Qt.AlignCenter)
        cam_preview.setStyleSheet("color: rgba(255,255,255,0.6); background: transparent;")
        cam_preview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        cam_layout.addWidget(cam_title)
        cam_layout.addWidget(cam_preview)
        grid.addWidget(self.camera_card, 0, 0)

        # Alarm card - sağ üst
        self.alarm_card = QFrame()
        self.alarm_card.setObjectName("alarm_card")
        self.alarm_card.setStyleSheet(self.alarm_card_style(active=False))
        alarm_layout = QVBoxLayout(self.alarm_card)
        alarm_top = QHBoxLayout()
        alarm_lbl = QLabel("Alarm")
        alarm_lbl.setFont(QFont("Sans", 14, QFont.Bold))
        alarm_top.addWidget(alarm_lbl)
        alarm_top.addStretch()
        self.alarm_button = QPushButton("ALARM AÇ")
        self.alarm_button.setCursor(Qt.PointingHandCursor)
        self.alarm_button.setFixedSize(140, 44)
        self.alarm_button.setStyleSheet(self.alarm_button_style(active=False))
        self.alarm_button.clicked.connect(self.on_alarm_pressed)
        alarm_top.addWidget(self.alarm_button)
        alarm_layout.addLayout(alarm_top)
        self.alarm_info = QLabel("Durum: Pasif\nSensörler: Kapalı\nKamera: Beklemede")
        self.alarm_info.setFont(QFont("Sans", 11))
        self.alarm_info.setStyleSheet("color: rgba(255,255,255,0.85); background: transparent;")
        alarm_layout.addStretch(1)
        alarm_layout.addWidget(self.alarm_info)
        grid.addWidget(self.alarm_card, 0, 1)

        # Map / ev krokisi - sol alt
        self.map_card = InfoCard("Ev Krokisi", "Küçük ev planı / sensör konumları buraya gelecek", height=220)
        grid.addWidget(self.map_card, 1, 0)

        # Status / log panel - sağ alt
        self.status_card = InfoCard("Sistem Bilgisi", "Panel hazır. Alarm pasif.")
        grid.addWidget(self.status_card, 1, 1)

        # make first column wider
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 1)

        root.addLayout(grid)
        root.addStretch(1)

    def start_clock(self):
        timer = QTimer(self)
        timer.timeout.connect(self.update_clock)
        timer.start(1000)
        self.update_clock()

    def update_clock(self):
        self.clock.setText(QTime.currentTime().toString("HH:mm:ss"))

    def on_alarm_pressed(self):
        if not self.alarm_active:
            # Alarm açılırken PIN sormuyor
            self.set_alarm_active(True)
        else:
            # Alarm kapatılırken PIN sor
            np = NumPad(self)
            if np.exec_() == QDialog.Accepted:
                self.set_alarm_active(False)

    def set_alarm_active(self, active: bool):
        self.alarm_active = active
        if active:
            self.alarm_card.setStyleSheet(self.alarm_card_style(active=True))
            self.alarm_button.setText("ALARM KAPAT")
            self.alarm_button.setStyleSheet(self.alarm_button_style(active=True))
            self.alarm_info.setText("Durum: Aktif\nSensörler: Aktif\nKamera: Devrede")
            self.status_card.content_lbl.setText("Alarm aktif. Tüm güvenlik sensörleri devrede.")
            self.camera_card.setStyleSheet("""
                QFrame#camera_card {
                    background: rgba(20,20,20,0.55);
                    border-radius: 12px;
                    border: 2px solid rgba(255,80,80,0.95);
                }
            """)
            self.flash_state = False
            self.alarm_flash_timer.start(500)
        else:
            self.alarm_card.setStyleSheet(self.alarm_card_style(active=False))
            self.alarm_button.setText("ALARM AÇ")
            self.alarm_button.setStyleSheet(self.alarm_button_style(active=False))
            self.alarm_info.setText("Durum: Pasif\nSensörler: Kapalı\nKamera: Beklemede")
            self.status_card.content_lbl.setText("Panel hazır. Alarm pasif.")
            self.camera_card.setStyleSheet("""
                QFrame#camera_card {
                    background: black;
                    border-radius: 12px;
                    border: 1px solid rgba(255,255,255,0.03);
                }
            """)
            self.alarm_flash_timer.stop()
            self.flash_state = False

    def flash_alarm(self):
        self.flash_state = not self.flash_state
        if self.flash_state:
            self.alarm_card.setStyleSheet("""
                QFrame#alarm_card {
                    background: rgba(255,0,0,0.15);
                    border-radius: 12px;
                    border: 2px solid rgba(255,80,80,0.95);
                }
            """)
        else:
            self.alarm_card.setStyleSheet("""
                QFrame#alarm_card {
                    background: rgba(0,0,0,0);
                    border-radius: 12px;
                    border: 2px solid rgba(255,80,80,0.95);
                }
            """)

    @staticmethod
    def alarm_card_style(active: bool) -> str:
        if active:
            return """
                QFrame#alarm_card {
                    background: rgba(0,0,0,0);
                    border-radius: 12px;
                    border: 2px solid rgba(255,80,80,0.9);
                }
                QLabel { color: white; background: transparent; }
            """
        else:
            return """
                QFrame#alarm_card {
                    background: rgba(255,255,255,0.03);
                    border-radius: 12px; border: 1px solid rgba(255,255,255,0.03);
                }
                QLabel { color: white; background: transparent; }
            """

    @staticmethod
    def alarm_button_style(active: bool) -> str:
        if active:
            return """
                QPushButton {
                    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #ff6b6b, stop:1 #ff3b3b);
                    color: white; border-radius: 22px; font-weight:bold;
                }
                QPushButton:pressed { background: #e63b3b; }
            """
        else:
            return """
                QPushButton {
                    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #3a3a3a, stop:1 #2a2a2a);
                    color: white; border-radius: 22px; font-weight:bold;
                }
                QPushButton:pressed { background: #4a4a4a; }
            """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainScreen()
    window.show()
    sys.exit(app.exec_())
