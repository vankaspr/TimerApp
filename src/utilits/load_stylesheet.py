import os
from pathlib import Path


def load_stylesheet():
    # Получаем абсолютный путь к директории со стилями
    style_dir = Path(__file__).parent.parent / "styles"
    css_file = style_dir / "styles.css"

    try:
        with open(css_file, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Ошибка: файл стилей не найден по пути {css_file}")
        return ""