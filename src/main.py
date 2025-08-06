import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from utilities import load_pixelify_font
from libs.logger import setup_logging, get_logger
from ui import TimerWindow


setup_logging()
logger = get_logger(__name__)


def main():
    try:
        logger.info("Starting application")

        app = QApplication(sys.argv)

        logger.debug("QApplication created")

        font_family = load_pixelify_font()
        if font_family:
            app.setFont(QFont(font_family, 24))

        window = TimerWindow()
        window.show()
        logger.info("Main window displayed")

        sys.exit(app.exec_())

    except Exception as e:
        logger.critical("Application failed", exc_info=True)
        raise Exception(f"error {e}")


if __name__ == "__main__":
    main()
