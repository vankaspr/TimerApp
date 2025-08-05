import logging
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTime
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTimeEdit,
    QLabel,
    QPushButton,
    QHBoxLayout,
)
from utilits.timer import TimerLogic
from utilits.load_stylesheet import load_stylesheet
from utilits.load_fonts import load_pixelify_font
from libs.logger import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


class TimerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Timer-App")
        self.setFixedSize(400, 300)

        self.setStyleSheet(load_stylesheet())

        # Экземпляр таймера
        self.timer = TimerLogic()
        self.timer.time_update.connect(self.update_display)
        self.timer.timer_finished.connect(self.on_timer_finished)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        # input time
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm:ss")
        self.time_edit.setTime(QTime(0, 1, 0))  # 00.01.00 default

        # Отображение времени
        self.time_label = QLabel("00:00:00")
        self.time_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Кнопки
        self.start_btn = QPushButton("start")
        self.pause_btn = QPushButton("pause")
        self.reset_btn = QPushButton("reset")

        # Горизонтальный layout для кнопок
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.reset_btn)

        # Добавляем всё в layout
        layout.addWidget(self.time_edit)
        layout.addWidget(self.time_label)
        layout.addLayout(btn_layout)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Подключаем кнопки
        self.start_btn.clicked.connect(self.start_timer)
        self.pause_btn.clicked.connect(self.pause_timer)
        self.reset_btn.clicked.connect(self.reset_timer)

    def start_timer(self):
        """start the timer with the selected time"""
        time = self.time_edit.time()
        self.timer.set_time(time.hour(), time.minute(), time.second())
        self.timer.start()
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)

    def pause_timer(self):
        """Pause"""
        self.timer.pause()
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)

    def reset_timer(self):
        """Reset"""
        self.timer.reset()
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)

    def update_display(self, time_str):
        """Update time display"""
        self.time_label.setText(time_str)

    def on_timer_finished(self):
        """Timer ending actions"""
        self.time_label.setText("00:00:00 ⏰")
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)


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
