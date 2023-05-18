import os
from pathlib import Path
import shlex
import subprocess
from utils import utils

PATH: Path = Path(__file__).parent

timeObjPath = PATH / "hid_time.dat"

# checking timer
try:
    utils.expose_file(timeObjPath)
except:
    if os.path.exists(os.path.join(PATH, "hid_time.dat")):
        utils.hide_file(timeObjPath)
        # sudoku if timer after hiding file again
        os.kill(os.getpid(), 9)
    else:
        # continue if no timer
        utils.set_wallpaper(PATH / "defaut_assets" / "default_win10.jpg")

if utils.is_windows():
    os.startfile("panic.bat")
elif utils.is_linux():
    # I'm no expert but here we are
    # Select all user python processes using files ending with .pyw in the command.
    # Select the pid.
    # Terminate it.
    subprocess.run(
        "for pid in $(ps -u $USER -ef | grep -E \"python.* *+.pyw\" | awk '{print $2}'); do echo $pid; kill -9 $pid; done",
        shell=True,
    )
