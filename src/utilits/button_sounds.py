from typing import Callable
from utilits import SoundPlayer


def sound_wrapper(
    sound_player: SoundPlayer,
    sound_name: str,
    target_func: Callable[[], None],
) -> Callable[[], None]:
    """Wrapper to play sound before executing a function"""

    def wrapper():
        try:
            sound_player.play(sound_name)
        except Exception as e:
            print(f"Error sound play: {e}")
        finally:
            target_func()

    return wrapper
