import pytest
from PyQt5.QtCore import QTime, Qt
from unittest.mock import MagicMock, call
from ui.window import TimerWindow


@pytest.fixture
def app(qtbot, monkeypatch):
    mock_player = MagicMock()
    mock_player.play = MagicMock()

    monkeypatch.setattr("ui.window.SoundPlayer", lambda: mock_player)
    monkeypatch.setattr(
        "ui.window.sound_wrapper", lambda sound_player, sound_name, func: func
    )
    monkeypatch.setattr("ui.window.get_random_image", MagicMock())

    test_app = TimerWindow()
    qtbot.addWidget(test_app)

    test_app.sound_player = mock_player
    return test_app


class TestTimerUI:

    def test_initial_state(self, app):
        """Проверка начального состояния интерфейса"""
        assert app.time_edit.time() == QTime(0, 0, 0)
        assert app.time_label.text() == "00:00:00"

        # Проверяем состояние кнопок
        assert app.start_btn.isEnabled()
        assert app.start_btn.text().lower() == "start"

    def test_start_timer(self, app, qtbot):
        """Проверка запуска таймера"""
        test_time = QTime(0, 0, 2)
        app.time_edit.setTime(test_time)

        qtbot.mouseClick(app.start_btn, Qt.LeftButton)

        assert not app.start_btn.isEnabled()
        assert app.pause_btn.isEnabled()
        assert app.time_label.text() == "00:00:02"

    def test_timer_finish(self, app, qtbot):
        """Проверка завершения таймера"""
        app.sound_player.play.reset_mock()

        app.time_edit.setTime(QTime(0, 0, 1))
        qtbot.mouseClick(app.start_btn, Qt.LeftButton)

        app.timer.timer.timeout.emit()
        app.timer.timer_finished.emit()

        assert app.start_btn.isEnabled()
        assert not app.pause_btn.isEnabled()

        app.sound_player.play.assert_called_once_with("end-timer")

    def test_timer_finish(self, app, qtbot):
        """Проверка завершения таймера"""

        app.time_edit.setTime(QTime(0, 0, 1))

        app.sound_player.play.reset_mock()

        qtbot.mouseClick(app.start_btn, Qt.LeftButton)

        app.timer.timer.timeout.emit()

        assert app.time_label.text() == "00:00:00"

        app.timer.timer_finished.emit()

        assert app.start_btn.isEnabled()
        assert not app.pause_btn.isEnabled()

        assert app.sound_player.play.call_count > 0
        assert call("end-timer") in app.sound_player.play.call_args_list

    def test_time_edit(self, app):
        """Тест редактирования времени"""
        new_time = QTime(1, 15, 30)
        app.time_edit.setTime(new_time)
        assert app.time_edit.time() == new_time

    def test_reset_functionality(self, app, qtbot):
        """Тест сброса таймера"""
        app.time_edit.setTime(QTime(0, 1, 30))
        qtbot.mouseClick(app.start_btn, Qt.LeftButton)
        qtbot.mouseClick(app.reset_btn, Qt.LeftButton)

        assert app.time_label.text() == "00:00:00"
        assert app.start_btn.isEnabled()

    def test_pause_functionality(self, app, qtbot):
        """Тест функционала паузы"""
        app.time_edit.setTime(QTime(0, 1, 0))
        qtbot.mouseClick(app.start_btn, Qt.LeftButton)
        qtbot.mouseClick(app.pause_btn, Qt.LeftButton)

        assert app.start_btn.isEnabled()
        assert not app.pause_btn.isEnabled()
