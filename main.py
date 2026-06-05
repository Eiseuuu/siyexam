import sys
import os
import requests

from dotenv import load_dotenv
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QFrame,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from dominantColor import getDominantColor


# =========================
# LOAD ENV + SECURE API KEY
# =========================
load_dotenv()

API_KEY = os.getenv("APININJA_API_KEY")

if not API_KEY:
    raise RuntimeError("Missing API key. Please set APININJA_API_KEY in .env file.")


# =========================
# API FUNCTION
# =========================
def fetch_random_image():
    url = "https://api.api-ninjas.com/v1/randomimage"

    response = requests.get(
        url,
        headers={
            "X-Api-Key": API_KEY,
            "Accept": "image/jpg"
        },
        timeout=10
    )

    response.raise_for_status()
    return response.content


# =========================
# IMAGE LOADER
# =========================
def load_pixmap(image_bytes):
    pixmap = QPixmap()
    pixmap.loadFromData(image_bytes)
    return pixmap


# =========================
# MAIN APP UI
# =========================
class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Color Identifier")
        self.resize(500, 600)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(24, 24, 24, 24)
        outer_layout.setAlignment(Qt.AlignCenter)

        self.main_container = QFrame()
        self.main_container.setFixedSize(560, 560)

        self.main_container.setStyleSheet("""
            QFrame {
                border: 1px solid #d0d0d0;
                border-radius: 18px;
                background: #ffffff;
            }
        """)

        main_layout = QVBoxLayout(self.main_container)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(18)

        # IMAGE LABEL
        self.label = QLabel("Click to load random image")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumHeight(300)
        self.label.setStyleSheet("""
            border: 1px solid #ececec;
            border-radius: 14px;
            background: #f7f7f7;
            color: #666;
        """)

        # BUTTON
        self.button = QPushButton("Get Random Image")
        self.button.clicked.connect(self.on_click)

        # COLOR LABEL
        self.color_label = QLabel("Dominant color")
        self.color_label.setAlignment(Qt.AlignCenter)

        # SWATCH
        self.color_swatch = QLabel()
        self.color_swatch.setFixedSize(28, 28)
        self.color_swatch.setStyleSheet("""
            border: 1px solid #999;
            border-radius: 8px;
            background: transparent;
        """)

        # RGB FIELD
        self.rgb_value = QLineEdit()
        self.rgb_value.setReadOnly(True)
        self.rgb_value.setAlignment(Qt.AlignCenter)
        self.rgb_value.setPlaceholderText("RGB(r, g, b)")

        # COLOR ROW
        color_row = QHBoxLayout()
        color_row.addWidget(self.color_swatch)
        color_row.addWidget(self.rgb_value)

        # LAYOUT
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.button)
        main_layout.addWidget(self.color_label)
        main_layout.addLayout(color_row)

        outer_layout.addWidget(self.main_container, alignment=Qt.AlignCenter)

    # =========================
    # BUTTON ACTION
    # =========================
    def on_click(self):
        try:
            self.label.setText("Loading...")

            image_bytes = fetch_random_image()
            pixmap = load_pixmap(image_bytes)

            dominant_color = getDominantColor(image_bytes)

            # DISPLAY IMAGE
            self.label.setPixmap(
                pixmap.scaled(
                    self.label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

            # FORMAT COLOR
            r, g, b = dominant_color
            rgb_text = f"RGB({r}, {g}, {b})"

            self.rgb_value.setText(rgb_text)

            self.color_swatch.setStyleSheet(
                f"""
                border: 1px solid #999;
                border-radius: 8px;
                background-color: rgb({r}, {g}, {b});
                """
            )

        except Exception as e:
            self.label.setText(f"Error: {str(e)}")
            self.rgb_value.clear()
            self.color_swatch.setStyleSheet("background: transparent;")


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())