import ctypes, os
ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(os.getcwd()) + '\\default_assets\\default_win10.jpg', 0)
os.startfile('panic.bat')