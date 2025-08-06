from PyQt5.QtCore import QTime, Qt
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTimeEdit,
    QLabel,
    QPushButton,
    QHBoxLayout,
)
from utilits import (
    load_stylesheet,
    TimerLogic,
    sound_wrapper,
    SoundPlayer,
    add_unified_sound_to_time_edit,
    get_random_image,
)


class TimerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Timer-App")
        self.setFixedSize(500, 400)

        self.sound_player = SoundPlayer()

        self.setStyleSheet(load_stylesheet())

        # Экземпляр таймера
        self.timer = TimerLogic()
        self.timer.time_update.connect(self.update_display)
        self.timer.timer_finished.connect(self.on_timer_finished)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        layout.setContentsMargins(20, 40, 20, 20)
        layout.setSpacing(20)

        # text
        text = QLabel("Set Time")
        text.setAlignment(Qt.AlignCenter)
        text.setStyleSheet(
            """
            QLabel {
                font-size: 48px;
                line-height: 58px;
                color: #364C84;
            }
            """
        )

        # input time
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm:ss")
        self.time_edit.setTime(QTime(0, 0, 0))  # 00.01.00 default
        layout.addWidget(self.time_edit)
        add_unified_sound_to_time_edit(
            time_edit=self.time_edit,
            sound_player=self.sound_player,
            sound_name="arrow-click",
        )

        # Отображение времени
        self.time_label = QLabel("00:00:00")
        self.time_label.setAlignment(
            Qt.AlignCenter
        )  # Центрирование текста внутри QLabel

        label_container = QWidget()
        label_layout = QHBoxLayout(label_container)
        label_layout.addStretch()
        label_layout.addWidget(self.time_label)

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
        layout.addWidget(text)
        layout.addWidget(self.time_edit)

        layout.addWidget(self.time_label)
        layout.addLayout(btn_layout)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Подключаем кнопки
        self.start_btn.clicked.connect(
            sound_wrapper(self.sound_player, "button-click", self.start_timer)
        )
        self.pause_btn.clicked.connect(
            sound_wrapper(self.sound_player, "button-click", self.pause_timer)
        )
        self.reset_btn.clicked.connect(
            sound_wrapper(self.sound_player, "button-click", self.reset_timer)
        )

    def start_timer(self):
        """start the timer with the selected time"""
        # Отображение времени
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
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.sound_player.play("end-timer")

        if not hasattr(self.time_label, "original_text"):
            self.time_label.original_text = "00:00:00"

        get_random_image(self.time_label, "media/images")
