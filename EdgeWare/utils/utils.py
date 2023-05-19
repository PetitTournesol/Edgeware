import sys
from enum import Enum


def is_windows() -> bool:
    return "win32" in sys.platform


def is_linux() -> bool:
    return "linux" in sys.platform

class DEPENDENCIES(str, Enum):
    FFMPEG = "FFMPEG"
    PORT_AUDIO = "PortAudio"

if is_linux():
    from .linux import *
elif is_windows():
    from .windows import *
else:
    raise RuntimeError("Unsupported operating system: {}".format(sys.platform))


class SCRIPTS(str, Enum):
    DISCORD_HANDLER = "disc_handler.pyw"
    POPUP = "popup.pyw"
    PANIC = "panic.pyw"


def run_script(*args: str | SCRIPTS):
    popen_args = [sys.executable, *args]

    subprocess.Popen(popen_args)


def run_discord_handler_script(*args: str):
    run_script(SCRIPTS.DISCORD_HANDLER, *args)


def run_popup_script(*args: str):
    run_script(SCRIPTS.POPUP, *args)


def run_panic_script(*args: str):
    run_script(SCRIPTS.PANIC, *args)
