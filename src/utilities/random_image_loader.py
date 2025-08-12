import os
import random
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from utilities.resource_path_helper import resource_path


def get_random_image(label: QLabel, image_dir: str = "media/images") -> None:
    try:

        original_size = label.size()
        original_policy = label.sizePolicy()
        original_text = label.text()
        original_stylesheet = label.styleSheet()

        resolved_image_dir = resource_path(image_dir)

        if not os.path.exists(resolved_image_dir):
            raise FileNotFoundError(f"Image directory not found: {resolved_image_dir}")

        images = [
            os.path.join(resolved_image_dir, f)
            for f in os.listdir(resolved_image_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        if not images:
            raise FileNotFoundError("No images found in directory")

        random_image_path = random.choice(images)

        pixmap = QPixmap(random_image_path)
        if pixmap.isNull():
            raise ValueError(f"Failed to load image: {random_image_path}")

        max_size = label.parent().height() // 4
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

        print(f"Tried to load from: {image_dir}")
        print(f"Resolved path: {resource_path(image_dir)}")


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
