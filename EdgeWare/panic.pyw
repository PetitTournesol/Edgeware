import os
from pathlib import Path
from multiprocessing.connection import Client
from array import array
from utils import utils
from panic_listener import ADDRESS, AUTH_KEY

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


with Client(ADDRESS, authkey=AUTH_KEY) as conn:
    conn.send("panic_close")
