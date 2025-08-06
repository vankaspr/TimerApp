import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from utilities import load_pixelify_font
from ui import TimerWindow


def main():
    try:
        app = QApplication(sys.argv)

        font_family = load_pixelify_font()
        if font_family:
            app.setFont(QFont(font_family, 24))

        window = TimerWindow()
        window.show()

        sys.exit(app.exec_())

    except Exception as e:
        raise Exception(f"error {e}")


if __name__ == "__main__":
    main()
