import sys
import requests
from io import BytesIO
from collections import Counter

from PIL import Image
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt


class RandomImageApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Random Image Dominant Color")
        self.resize(600, 500)

        self.layout = QVBoxLayout(self)

        self.image_label = QLabel("Click the button to load an image")
        self.image_label.setAlignment(Qt.AlignCenter)

        self.color_preview = QLabel()
        self.color_preview.setFixedSize(120, 120)
        self.color_preview.setStyleSheet("background: white; border: 1px solid black;")

        self.color_label = QLabel("Dominant Color: N/A")
        self.color_label.setAlignment(Qt.AlignCenter)

        self.button = QPushButton("Get Random Image")
        self.button.clicked.connect(self.load_random_image)

        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.color_preview, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.color_label)
        self.layout.addWidget(self.button)

    def load_random_image(self):
        try:
            # Random image API
            response = requests.get(
                "https://picsum.photos/500",
                timeout=10
            )

            image = Image.open(BytesIO(response.content)).convert("RGB")

            # Display image
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)

            self.image_label.setPixmap(
                pixmap.scaled(
                    500,
                    350,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

            dominant = self.get_dominant_color(image)

            r, g, b = dominant

            self.color_label.setText(
                f"Dominant Color: RGB({r}, {g}, {b})"
            )

            self.color_preview.setStyleSheet(
                f"""
                background-color: rgb({r}, {g}, {b});
                border: 1px solid black;
                """
            )

        except Exception as e:
            self.color_label.setText(f"Error: {e}")

    def get_dominant_color(self, image):
        """
        Resize image for faster processing and
        return the most common RGB value.
        """
        small = image.resize((100, 100))

        pixels = list(small.getdata())

        counter = Counter(pixels)

        dominant_color = counter.most_common(1)[0][0]

        return dominant_color


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = RandomImageApp()
    window.show()

    sys.exit(app.exec())