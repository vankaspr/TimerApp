from PyQt5.QtGui import QFontDatabase

from pathlib import Path


def load_pixelify_font():
    """Надёжная загрузка Pixelify Sans с диагностикой"""
    try:
        # Получаем абсолютный путь (кросс-платформенно)
        font_path = Path(__file__).parent.parent / "fonts" / "PixelifySans.ttf"
        font_path = font_path.resolve()  # Преобразуем в абсолютный путь

        print(f"🔄 Пытаемся загрузить шрифт из: {font_path}")

        # Проверка существования файла
        if not font_path.exists():
            available = list(font_path.parent.glob("*"))
            raise FileNotFoundError(
                f"Файл шрифта не найден. Доступные файлы: {available}"
            )

        # Загрузка шрифта
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        if font_id == -1:
            raise RuntimeError(
                f"Qt не смог загрузить файл. Поддерживаемые форматы: {QFontDatabase.supportedFontFormats()}"
            )

        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if not font_families:
            raise ValueError("Шрифт загружен, но не возвращает имя семейства")

        print(f"✅ Успешно загружен шрифт: {font_families[0]}")
        return font_families[0]

    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        return None
