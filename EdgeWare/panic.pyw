import ctypes
import os
import pathlib
PATH = str(pathlib.Path(__file__).parent.absolute())

timeObjPath = os.path.join(PATH, 'hid_time.dat')
HIDDEN_ATTR = 0x02
SHOWN_ATTR  = 0x08
#checking timer
try:
    ctypes.windll.kernel32.SetFileAttributesW(timeObjPath, SHOWN_ATTR)
except:
    ''
if os.path.exists(os.path.join(PATH, 'hid_time.dat')):
    ctypes.windll.kernel32.SetFileAttributesW(timeObjPath, HIDDEN_ATTR)
    #sudoku if timer after hiding file again
    os.kill(os.getpid(), 9)
else:
    #continue if no timer
    ctypes.windll.user32.SystemParametersInfoW(20, 0, PATH + '\\default_assets\\default_win10.jpg', 0)

os.startfile('panic.bat')