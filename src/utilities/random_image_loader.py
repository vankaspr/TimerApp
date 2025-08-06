import os
import random
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSizePolicy


def get_random_image(label: QLabel, image_dir: str = "media/images") -> None:
    try:

        original_size = label.size()
        original_policy = label.sizePolicy()
        original_text = label.text()
        original_stylesheet = label.styleSheet()

        images = [
            f for f in os.listdir(image_dir) if f.endswith((".png", ".jpg", "jpeg"))
        ]

        if images:

            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            label.setAlignment(Qt.AlignCenter)

            random_image = random.choice(images)
            pixmap = QPixmap(os.path.join(image_dir, random_image))

            max_size = label.parent().height() // 3
            scaled_pixmap = pixmap.scaled(
                max_size, max_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )

            label.setPixmap(scaled_pixmap)

            QTimer.singleShot(
                5000,
                lambda: restore_label(
                    label,
                    original_size,
                    original_policy,
                    original_text,
                    original_stylesheet,
                ),
            )

    except Exception as e:
        print(f"Image load error: {e}")
        label.setText("⏰")


def restore_label(
    label,
    original_size,
    original_policy,
    original_text,
    original_stylesheet,
):
    label.clear()
    label.setPixmap(QPixmap())
    label.setSizePolicy(original_policy)
    label.resize(original_size)
    label.setText(original_text)
    label.setStyleSheet(original_stylesheet)
    label.setAlignment(Qt.AlignCenter)
