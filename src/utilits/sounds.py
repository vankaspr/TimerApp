from pathlib import Path
from PyQt5.QtMultimedia import QSound


class SoundPlayer:
    def __init__(self):

        base_dir = Path(__file__).parent.parent
        sound_dir = base_dir / "media" / "sounds"

        self.sounds = {
            "arrow-click": QSound(str(sound_dir / "arrows-click.wav")),
            "button-click": QSound(str(sound_dir / "buttons-click.wav")),
            "end-timer": QSound(str(sound_dir / "end-timer.wav")),
        }

    def play(self, sound_name):
        try:
            self.sounds[sound_name].play()
        except Exception as e:
            print(f"error: cant play sounds / sounds not found {e}")
            return ""
