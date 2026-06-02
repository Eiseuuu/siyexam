import sys
import requests
import os

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

load_dotenv()

API_KEY = os.getenv("APININJA_API_KEY")


def fetch_random_image():
    url = "https://api.api-ninjas.com/v1/randomimage"

    response = requests.get(
        url,
        headers={
            "X-Api-Key": API_KEY,
            "Accept": "image/jpg"
        }
    )

    return response.content


def load_pixmap(image_bytes):
    pixmap = QPixmap()
    pixmap.loadFromData(image_bytes)
    return pixmap


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Color Identifier")
        self.resize(500, 600)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(24, 24, 24, 24)
        outer_layout.setAlignment(Qt.AlignCenter)

        self.main_container = QFrame()
        self.main_container.setObjectName("mainContainer")
        self.main_container.setFixedSize(560, 560)
        self.main_container.setStyleSheet(
            """
            QFrame#mainContainer {
                border: 1px solid #d0d0d0;
                border-radius: 18px;
                background: #ffffff;
            }
            QFrame#actionBox {
                border: 1px solid #e0e0e0;
                border-radius: 14px;
                background: #fafafa;
            }
            QLabel#imageLabel {
                border: 1px solid #ececec;
                border-radius: 14px;
                background: #f7f7f7;
                color: #666;
            }
            QLabel#swatch {
                border: 1px solid #999;
                border-radius: 8px;
                background: transparent;
            }
            QLineEdit#rgbValue {
                border: 1px solid #d6d6d6;
                border-radius: 10px;
                padding: 8px 10px;
                background: #ffffff;
            }
            """
        )

        main_layout = QVBoxLayout(self.main_container)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(18)

        self.label = QLabel("Click to load random image")
        self.label.setObjectName("imageLabel")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setMinimumHeight(300)

        self.action_row = QHBoxLayout()
        self.action_row.setSpacing(16)

        self.left_div = QFrame()
        self.left_div.setObjectName("actionBox")
        left_layout = QVBoxLayout(self.left_div)
        left_layout.setContentsMargins(16, 16, 16, 16)
        left_layout.addStretch(1)

        self.button = QPushButton("Get Random Image")
        self.button.clicked.connect(self.on_click)
        left_layout.addWidget(self.button)
        left_layout.addStretch(1)

        self.right_div = QFrame()
        self.right_div.setObjectName("actionBox")
        right_layout = QVBoxLayout(self.right_div)
        right_layout.setContentsMargins(16, 16, 16, 16)
        right_layout.setSpacing(10)
        right_layout.addStretch(1)

        self.color_label = QLabel("Dominant color")
        self.color_label.setAlignment(Qt.AlignCenter)

        self.color_row = QHBoxLayout()
        self.color_row.setSpacing(10)
        self.color_row.setAlignment(Qt.AlignCenter)

        self.color_swatch = QLabel()
        self.color_swatch.setObjectName("swatch")
        self.color_swatch.setFixedSize(28, 28)

        self.rgb_value = QLineEdit()
        self.rgb_value.setObjectName("rgbValue")
        self.rgb_value.setReadOnly(True)
        self.rgb_value.setAlignment(Qt.AlignCenter)
        self.rgb_value.setPlaceholderText("rgb(r, g, b)")
        self.rgb_value.setMinimumWidth(170)

        self.color_row.addWidget(self.color_swatch)
        self.color_row.addWidget(self.rgb_value)

        right_layout.addWidget(self.color_label)
        right_layout.addLayout(self.color_row)
        right_layout.addStretch(1)

        self.action_row.addWidget(self.left_div)
        self.action_row.addWidget(self.right_div)

        main_layout.addWidget(self.label)
        main_layout.addLayout(self.action_row)

        outer_layout.addWidget(self.main_container, alignment=Qt.AlignCenter)

    def on_click(self):
        try:
            self.label.setText("Loading...")

            image_bytes = fetch_random_image()
            pixmap = load_pixmap(image_bytes)
            dominant_color = getDominantColor(image_bytes)
            rgb_text = f"rgb{dominant_color}"

            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)
            self.color_label.setText("Dominant color")
            self.rgb_value.setText(rgb_text)
            self.color_swatch.setStyleSheet(
                f"border: 1px solid #999; border-radius: 8px; background-color: rgb{dominant_color};"
            )

        except Exception as e:
            self.label.setText(f"Error: {str(e)}")
            self.color_label.setText("")
            self.rgb_value.setText("")
            self.color_swatch.setStyleSheet("border: 1px solid #999; border-radius: 8px; background: transparent;")



app = QApplication(sys.argv)
window = App()
window.show()

sys.exit(app.exec())