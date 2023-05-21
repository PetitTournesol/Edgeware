import ctypes
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from utils.area import Area
import logging

user = ctypes.windll.user32


class RECT(ctypes.Structure):  # rect class for containing monitor info
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]

    def dump(self) -> tuple[int, int, int, int]:
        return tuple(map(int, (self.left, self.top, self.right, self.bottom)))


def get_monitors():
    retval = []
    CBFUNC = ctypes.WINFUNCTYPE(
        ctypes.c_int,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.POINTER(RECT),
        ctypes.c_double,
    )

    def cb(hMonitor, hdcMonitor, lprcMonitor, dwData):
        r = lprcMonitor.contents
        data = [hMonitor]
        data.append(r.dump())
        retval.append(data)
        return 1

    cbfunc = CBFUNC(cb)
    _ = user.EnumDisplayMonitors(0, 0, cbfunc, 0)
    return retval


class MONITORINFO(
    ctypes.Structure
):  # unneeded for this, but i don't want to rework the entire thing because i'm stupid
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("rcMonitor", RECT),
        ("rcWork", RECT),
        ("dwFlags", ctypes.c_ulong),
    ]


def monitor_areas():  # all that matters from this is list(mapObj[monitor index][1])[k]; this is the list of monitor dimensions
    areas: list[Area] = []
    monitors = get_monitors()

    for hMonitor, _ in monitors:
        data = [hMonitor]
        mi = MONITORINFO()
        mi.cbSize = ctypes.sizeof(MONITORINFO)
        mi.rcMonitor = RECT()
        mi.rcWork = RECT()
        _ = user.GetMonitorInfoA(hMonitor, ctypes.byref(mi))
        work_area = mi.rcWork.dump()
        x, y = work_area[0], work_area[1]
        areas.append(Area(x, y, work_area[2] - x, work_area[3] - y))

    return areas


def set_wallpaper(wallpaper_path: Path | str):
    if isinstance(wallpaper_path, Path):
        wallpaper_path = str(wallpaper_path.absolute())

    ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 0)


HIDDEN_ATTR = 0x02
SHOWN_ATTR = 0x08


def hide_file(path: Path | str):
    if isinstance(path, Path):
        path = str(path.absolute())
    ctypes.windll.kernel32.SetFileAttributesW(path, HIDDEN_ATTR)


def expose_file(path: Path | str):
    if isinstance(path, Path):
        path = str(path.absolute())
    ctypes.windll.kernel32.SetFileAttributesW(path, SHOWN_ATTR)


def _create_shortcut_script(
    path: Path,
    icon: str,
    script: str,
    title: str | None = None,
    startup_path: str | None = None,
):
    # strings for batch script to write vbs script to create shortcut on desktop
    # stupid and confusing? yes. the only way i could find to do this? also yes.
    if title is None:
        title = f"Edgeware_{script}"

    if startup_path is None:
        startup_path = "%USERPROFILE%\\Desktop"

    path_str = str(path.absolute())

    return [
        "@echo off\n" 'set SCRIPT="%TEMP%\\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"\n',
        'echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%\n',
        f'echo sLinkFile = "{startup_path}\\{title}.lnk" >> %SCRIPT%\n',
        "echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%\n",
        f'echo oLink.WorkingDirectory = "{path_str}\\" >> %SCRIPT%\n',
        f'echo oLink.IconLocation = "{path_str}\\default_assets\\{icon}_icon.ico" >> %SCRIPT%\n',
        f'echo oLink.TargetPath = "{sys.executable}" >> %SCRIPT%\n',
        f'echo oLink.Arguments = "{path_str}\\{script}" >> %SCRIPT%\n',
        "echo oLink.Save >> %SCRIPT%\n",
        "cscript /nologo %SCRIPT%\n",
        "del %SCRIPT%",
    ]


def does_desktop_shortcut_exists(name: str):
    file = Path(name)
    return Path(
        os.path.expanduser("~/Desktop") / file.with_name(f"{file.name}.lnk")
    ).exists()


def make_shortcut(
    path: Path,
    icon: str,
    script: str,
    title: str | None = None,
    startup_path: str | None = None,
) -> bool:
    success = False
    with tempfile.NamedTemporaryFile("w", suffix=".bat", delete=False, ) as bat:
        bat.writelines(
            _create_shortcut_script(path, icon, script, title, startup_path)
        )  # write built shortcut script text to temporary batch file

    try:
        logging.info(f"making shortcut to {script}")
        subprocess.run(bat.name)
        success = True
    except Exception as e:
        print("failed")
        logging.warning(
            f"failed to call or remove temp batch file for making shortcuts\n\tReason: {e}"
        )
    
    if os.path.exists(bat.name):
        os.remove(bat.name)

    return success


def toggle_run_at_startup(path: Path, state: bool):
    # FIXME: Find a crossplatform way to add edgeware to startup aplication
    try:
        startup_path = os.path.expanduser(
            "~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
        )
        logging.info(f"trying to toggle startup bat to {state}")
        if state:
            make_shortcut(path, "default", "start.pyw", "EdgeWare", startup_path)
            logging.info("toggled startup run on.")
        else:
            os.remove(os.path.join(startup_path, "edgeware.lnk"))
            logging.info("toggled startup run off.")
    except Exception as e:
        errText = (
            str(e)
            .lower()
            .replace(
                os.environ["USERPROFILE"].lower().replace("\\", "\\\\"),
                "[USERNAME_REDACTED]",
            )
        )
        logging.warning(f"failed to toggle startup bat.\n\tReason: {errText}")
        print("uwu")
