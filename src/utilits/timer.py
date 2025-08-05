from PyQt5.QtCore import QTimer, QTime, QObject, pyqtSignal

class TimerLogic(QObject):

    time_update = pyqtSignal(str)
    timer_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_time)
        self.time_left = QTime(0,0,0)
        self.is_running = False

    def set_time(self, hours, minutes, seconds):
        """Set Time"""
        self.time_left = QTime(hours, minutes, seconds)
        self._emit_time()

    def start(self):
        """Start Timer"""
        if not self.is_running and self.time_left > QTime(0,0,0):
            self.timer.start(1000)
            self.is_running = True

    def pause(self):
        """Pause Timer"""
        if self.is_running:
            self.timer.stop()
            self.is_running = False

    def reset(self):
        """Reset Time"""
        self.timer.stop()
        self.is_running = False
        self.time_left = QTime(0,0,0)
        self._emit_time()

    def _update_time(self):
        """Update time (calling every second)"""
        self.time_left = self.time_left.addSecs(-1)
        self._emit_time()

        if self.time_left == QTime(0,0,0):
            self.timer.stop()
            self.is_running = False
            self.timer_finished.emit()

    def _emit_time(self):
        """Delivering time in UI"""
        self.time_update.emit(self.time_left.toString("HH:mm:ss"))






