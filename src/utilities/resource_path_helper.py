import os
import sys


def resource_path(relative_path):
    """Получает абсолютный путь к ресурсу"""
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative_path)

    if not os.path.exists(full_path):
        print(f"⚠️ Ресурс не найден: {full_path}")
        print(f"Искал по пути: {relative_path}")

    return full_path
