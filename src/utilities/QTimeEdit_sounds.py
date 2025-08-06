from typing import Optional
from PyQt5.QtCore import QEvent, QObject
from PyQt5.QtWidgets import QTimeEdit
from utilities import SoundPlayer


class TimeEditSoundFilter(QObject):
    def __init__(
        self,
        sound_player: SoundPlayer,
        sound_name: str,
        parent: Optional[QObject] = None,
    ):
        super().__init__()
        self.sound_player = sound_player
        self.sound_name = sound_name

    def eventFilter(
        self,
        obj: QObject,
        event: QEvent,
    ) -> bool:
        if event.type() == QEvent.MouseButtonPress:
            self.sound_player.play(self.sound_name)
        return super().eventFilter(obj, event)


def add_unified_sound_to_time_edit(
    time_edit: QTimeEdit, sound_player: SoundPlayer, sound_name: str
) -> None:

    sound_filter = TimeEditSoundFilter(sound_player, sound_name, time_edit)
    time_edit.installEventFilter(sound_filter)

    original_step_by = time_edit.stepBy

    def wrapper_step_by(steps: int):
        sound_player.play(sound_name)
        original_step_by(steps)

    time_edit.stepBy = wrapper_step_by
