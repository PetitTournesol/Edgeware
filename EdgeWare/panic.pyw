import ctypes, os, pathlib
ctypes.windll.user32.SystemParametersInfoW(20, 0, str(pathlib.Path(__file__).parent.absolute()) + '\\default_assets\\default_win10.jpg', 0)
os.startfile('panic.bat')