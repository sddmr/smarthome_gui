import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout,
    QGridLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QGraphicsBlurEffect
)
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt

from mainscreen import MainScreen  # diğer ekranı içe aktar

PIN = "0000"  # Doğru PIN


class LockScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lock Screen")
        self.setGeometry(0, 0, 1920, 1080)

        # --- Arka plan resmi ---
        self.bg_pix = QPixmap("Back.jpg")
        if self.bg_pix.isNull():
            self.setStyleSheet("background-color: #2c2c2c;")
        else:
            self.set_background()

        # Ana dikey layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)

        # Spacer üstte
        main_layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # PIN giriş alanı
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setMaxLength(6)
        self.pin_input.setAlignment(Qt.AlignCenter)
        self.pin_input.setFont(QFont("Arial", 28, QFont.Bold))
        self.pin_input.setFixedWidth(300)
        self.pin_input.setStyleSheet(
            "QLineEdit { background-color: rgba(0,0,0,100); color: white; border-radius: 12px; padding: 15px; }"
        )
        main_layout.addWidget(self.pin_input, alignment=Qt.AlignHCenter)

        # NumPad düzeni
        grid = QGridLayout()
        grid.setSpacing(10)
        buttons = [
            ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
            ("←", 3, 0), ("0", 3, 1), ("OK", 3, 2)
        ]

        for text, row, col in buttons:
            btn = QPushButton(text)
            btn.setFont(QFont("Arial", 20, QFont.Bold))
            btn.setFixedSize(90, 75)

            # Blur efekti
            blur = QGraphicsBlurEffect()
            blur.setBlurRadius(2)
            btn.setGraphicsEffect(blur)

            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 60);
                    color: white;
                    border: 1px solid rgba(255,255,255,40);
                    border-radius: 12px;
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 100);
                }
            """)

            btn.clicked.connect(self.handle_button)
            grid.addWidget(btn, row, col)

        # Numpad container
        numpad_container = QHBoxLayout()
        numpad_container.setSpacing(0)
        numpad_container.addStretch()
        numpad_container.addLayout(grid)
        numpad_container.addStretch()

        main_layout.addLayout(numpad_container)

        # Spacer altta
        main_layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(main_layout)

    def set_background(self):
        """Resmi orantılı şekilde arka plana yerleştir"""
        scaled_pix = self.bg_pix.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scaled_pix))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def resizeEvent(self, event):
        if hasattr(self, 'bg_pix') and not self.bg_pix.isNull():
            self.set_background()
        super().resizeEvent(event)

    def handle_button(self):
        sender = self.sender().text()
        if sender == "Del":
            self.pin_input.backspace()
        elif sender == "OK":
            if self.pin_input.text() == PIN:
                # PIN doğru → MainScreen aç
                self.main = MainScreen()
                self.main.show()
                self.close()
            else:
                self.pin_input.clear()
        else:
            self.pin_input.setText(self.pin_input.text() + sender)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LockScreen()
    window.show()
    sys.exit(app.exec_())
