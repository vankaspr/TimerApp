import unittest
from PyQt5.QtCore import QTime
from PyQt5.QtTest import QSignalSpy
from utilities import TimerLogic


class TestTimerLogic(unittest.TestCase):
    def setUp(self):
        """Инициализация таймера перед каждым тестом"""
        self.timer = TimerLogic()

    def test_set_time(self):
        """Тест установки времени"""
        self.timer.set_time(1, 30, 15)
        self.assertEqual(self.timer.time_left, QTime(1, 30, 15))

    def test_start_timer(self):
        """Тест запуска таймера"""
        self.timer.set_time(0, 0, 2)
        spy = QSignalSpy(self.timer.time_update)
        self.timer.start()
        self.assertTrue(self.timer.is_running)
        self.timer.timer.timeout.emit()
        self.assertEqual(len(spy), 1)
        self.assertEqual(self.timer.time_left, QTime(0, 0, 1))

    def test_pause_timer(self):
        """Тест паузы таймера"""
        self.timer.set_time(0, 1, 0)
        self.timer.start()
        self.timer.pause()
        self.assertFalse(self.timer.is_running)
        self.assertFalse(self.timer.timer.isActive())

    def test_reset_timer(self):
        """Тест сброса таймера"""
        self.timer.set_time(0, 5, 0)
        self.timer.start()
        self.timer.reset()
        self.assertEqual(self.timer.time_left, QTime(0, 0, 0))
        self.assertFalse(self.timer.is_running)
        self.assertFalse(self.timer.timer.isActive())

    def test_timer_finish(self):
        """Тест завершения таймера"""
        self.timer.set_time(0, 0, 1)
        finish_spy = QSignalSpy(self.timer.timer_finished)
        time_spy = QSignalSpy(self.timer.time_update)

        self.timer.start()
        self.timer.timer.timeout.emit()  # 1 -> 0

        self.assertEqual(len(time_spy), 1)
        self.assertEqual(len(finish_spy), 1)
        self.assertEqual(self.timer.time_left, QTime(0, 0, 0))
        self.assertFalse(self.timer.is_running)

    def test_time_update_signal(self):
        """Тест сигнала обновления времени"""
        self.timer.set_time(0, 0, 3)
        spy = QSignalSpy(self.timer.time_update)

        self.timer.start()
        self.timer.timer.timeout.emit()  # 3 -> 2

        self.assertEqual(len(spy), 1)
        self.assertEqual(spy[0][0], "00:00:02")

    def test_multiple_updates(self):
        self.timer.set_time(0, 0, 3)
        spy = QSignalSpy(self.timer.time_update)

        self.timer.start()
        # Эмулируем 3 срабатывания таймера
        for _ in range(3):
            self.timer.timer.timeout.emit()

        self.assertEqual(len(spy), 3)
        self.assertEqual(spy[0][0], "00:00:02")
        self.assertEqual(spy[1][0], "00:00:01")
        self.assertEqual(spy[2][0], "00:00:00")

    def test_start_with_zero_time(self):
        self.timer.set_time(0, 0, 0)
        self.timer.start()
        self.assertFalse(self.timer.is_running)

    def test_time_formatting(self):
        self.timer.set_time(1, 5, 30)
        self.assertEqual(self.timer.time_left.toString("HH:mm:ss"), "01:05:30")
