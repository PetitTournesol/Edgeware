import codecs
from configparser import ConfigParser
import os
from pathlib import Path
import re
import shlex
import sys
from tkinter import messagebox
from Xlib.display import Display
from Xlib.ext import randr
import subprocess
from .dependencies import DEPENDENCIES
from .area import Area


def find_mode(id, modes):
    for mode in modes:
        if id == mode.id:
            return "{}x{}".format(mode.width, mode.height)


def get_monitors():
    display = Display()
    info = display.screen(0)
    window = info.root

    monitors = []

    res = randr.get_screen_resources(window)
    for output in res.outputs:
        params = display.xrandr_get_output_info(output, res.config_timestamp)
        if not params.crtc:
            continue
        crtc = display.xrandr_get_crtc_info(params.crtc, res.config_timestamp)
        monitors.append(crtc)

    return monitors


def monitor_areas():  # all that matters from this is list(mapObj[monitor index][1])[k]; this is the list of monitor dimensions
    areas: list[Area] = []
    for monitor in get_monitors():
        areas.append(
            Area(
                monitor.x,
                monitor.y,
                monitor.width,
                monitor.height,
            )
        )

    return areas


def hide_file(path: Path | str):
    if isinstance(path, str):
        path = Path(path)
    hidden_path = path.parent / f".{path.name}"
    if path.exists():
        path.rename(hidden_path)


def expose_file(path: Path | str):
    if isinstance(path, str):
        path = Path(path)
    hidden_path = path.parent / f".{path.name}"
    if hidden_path.exists():
        hidden_path.rename(path)


def check_dependencies() -> tuple[list[DEPENDENCIES], str]:
    missing_dependencies: list[DEPENDENCIES] = []
    messages: list[str] = []
    try:
        subprocess.check_output(["which", "ffmpeg"])
    except Exception as e:
        missing_dependencies.append(DEPENDENCIES.FFMPEG)
        messages.append("Couldn't find dependency FFMPEG.")

    try:
        import sounddevice
    except Exception as e:
        if len(e.args) == 1 and e.args[0] == "PortAudio library not found":
            missing_dependencies.append(DEPENDENCIES.PORT_AUDIO)
            messages.append(
                f"{e.args[0]}(Search for: 'libportaudio2' or 'libportaudio-dev')"
            )

    message = ""
    if messages:
        message = "\n".join((f"- {msg}" for msg in messages))
        messagebox.showerror("Missing dependencies", message)

    return missing_dependencies, message


first_run = True


def set_wallpaper(wallpaper_path: Path | str):
    global first_run
    if isinstance(wallpaper_path, Path):
        wallpaper_path = str(wallpaper_path.absolute())

    # Modified source from (Martin Hansen): https://stackoverflow.com/a/21213504
    # Note: There are two common Linux desktop environments where
    # I have not been able to set the desktop background from
    # command line: KDE, Enlightenment
    desktop_env = _get_desktop_environment()
    try:
        if desktop_env in ["gnome", "unity", "cinnamon"]:
            uri = "'file://%s'" % wallpaper_path
            args = [
                "gsettings",
                "set",
                "org.gnome.desktop.background",
                "picture-uri",
                uri,
            ]
            subprocess.Popen(args)
            args = [
                "gsettings",
                "set",
                "org.gnome.desktop.background",
                "picture-uri-dark",
                uri,
            ]
            subprocess.Popen(args)
        elif desktop_env == "mate":
            try:  # MATE >= 1.6
                # info from http://wiki.mate-desktop.org/docs:gsettings
                args = [
                    "gsettings",
                    "set",
                    "org.mate.background",
                    "picture-filename",
                    "'%s'" % wallpaper_path,
                ]
                subprocess.Popen(args)
            except:  # MATE < 1.6
                # From https://bugs.launchpad.net/variety/+bug/1033918
                args = [
                    "mateconftool-2",
                    "-t",
                    "string",
                    "--set",
                    "/desktop/mate/background/picture_filename",
                    '"%s"' % wallpaper_path,
                ]
                subprocess.Popen(args)
        elif desktop_env == "gnome2":  # Not tested
            # From https://bugs.launchpad.net/variety/+bug/1033918
            args = [
                "gconftool-2",
                "-t",
                "string",
                "--set",
                "/desktop/gnome/background/picture_filename",
                '"%s"' % wallpaper_path,
            ]
            subprocess.Popen(args)
        ## KDE4 is difficult
        ## see http://blog.zx2c4.com/699 for a solution that might work
        elif desktop_env in ["kde3", "trinity"]:
            # From http://ubuntuforums.org/archive/index.php/t-803417.html
            args = (
                'dcop kdesktop KBackgroundIface setWallpaper 0 "%s" 6' % wallpaper_path
            )
            subprocess.Popen(args, shell=True)
        elif desktop_env == "xfce4":
            # From http://www.commandlinefu.com/commands/view/2055/change-wallpaper-for-xfce4-4.6.0
            if first_run:
                args0 = [
                    "xfconf-query",
                    "-c",
                    "xfce4-desktop",
                    "-p",
                    "/backdrop/screen0/monitor0/image-path",
                    "-s",
                    wallpaper_path,
                ]
                args1 = [
                    "xfconf-query",
                    "-c",
                    "xfce4-desktop",
                    "-p",
                    "/backdrop/screen0/monitor0/image-style",
                    "-s",
                    "3",
                ]
                args2 = [
                    "xfconf-query",
                    "-c",
                    "xfce4-desktop",
                    "-p",
                    "/backdrop/screen0/monitor0/image-show",
                    "-s",
                    "true",
                ]
                subprocess.Popen(args0)
                subprocess.Popen(args1)
                subprocess.Popen(args2)
            args = ["xfdesktop", "--reload"]
            subprocess.Popen(args)
        elif (
            desktop_env == "razor-qt"
        ):  # TODO: implement reload of desktop when possible
            if first_run:
                desktop_conf = ConfigParser()
                # Development version
                desktop_conf_file = os.path.join(
                    _get_config_dir("razor"), "desktop.conf"
                )
                if os.path.isfile(desktop_conf_file):
                    config_option = r"screens\1\desktops\1\wallpaper"
                else:
                    desktop_conf_file = os.path.expanduser(".razor/desktop.conf")
                    config_option = r"desktops\1\wallpaper"
                desktop_conf.read(os.path.join(desktop_conf_file))
                try:
                    if desktop_conf.has_option(
                        "razor", config_option
                    ):  # only replacing a value
                        desktop_conf.set("razor", config_option, wallpaper_path)
                        with codecs.open(
                            desktop_conf_file,
                            "w",
                            encoding="utf-8",
                            errors="replace",
                        ) as f:
                            desktop_conf.write(f)
                except:
                    pass
            else:
                # TODO: reload desktop when possible
                pass
        elif desktop_env in ["fluxbox", "jwm", "openbox", "afterstep"]:
            # http://fluxbox-wiki.org/index.php/Howto_set_the_background
            # used fbsetbg on jwm too since I am too lazy to edit the XML configuration
            # now where fbsetbg does the job excellent anyway.
            # and I have not figured out how else it can be set on Openbox and AfterSTep
            # but fbsetbg works excellent here too.
            try:
                args = ["fbsetbg", wallpaper_path]
                subprocess.Popen(args)
            except:
                sys.stderr.write("ERROR: Failed to set wallpaper with fbsetbg!\n")
                sys.stderr.write("Please make sre that You have fbsetbg installed.\n")
        elif desktop_env == "icewm":
            # command found at http://urukrama.wordpress.com/2007/12/05/desktop-backgrounds-in-window-managers/
            args = ["icewmbg", wallpaper_path]
            subprocess.Popen(args)
        elif desktop_env == "blackbox":
            # command found at http://blackboxwm.sourceforge.net/BlackboxDocumentation/BlackboxBackground
            args = ["bsetbg", "-full", wallpaper_path]
            subprocess.Popen(args)
        elif desktop_env == "lxde":
            args = "pcmanfm --set-wallpaper %s --wallpaper-mode=scaled" % wallpaper_path
            subprocess.Popen(args, shell=True)
        elif desktop_env == "windowmaker":
            # From http://www.commandlinefu.com/commands/view/3857/set-wallpaper-on-windowmaker-in-one-line
            args = "wmsetbg -s -u %s" % wallpaper_path
            subprocess.Popen(args, shell=True)
        ## NOT TESTED BELOW - don't want to mess things up ##
        # elif desktop_env=="enlightenment": # I have not been able to make it work on e17. On e16 it would have been something in this direction
        #    args = "enlightenment_remote -desktop-bg-add 0 0 0 0 %s" % wallpaper_path
        #    subprocess.Popen(args,shell=True)
        # elif desktop_env=="windows": #Not tested since I do not run this on Windows
        #    #From https://stackoverflow.com/questions/1977694/change-desktop-background
        #    import ctypes
        #    SPI_SETDESKWALLPAPER = 20
        #    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, wallpaper_path , 0)
        # elif desktop_env=="mac": #Not tested since I do not have a mac
        #    #From https://stackoverflow.com/questions/431205/how-can-i-programatically-change-the-background-in-mac-os-x
        #    try:
        #        from appscript import app, mactypes
        #        app('Finder').desktop_picture.set(mactypes.File(wallpaper_path))
        #    except ImportError:
        #        #import subprocess
        #        SCRIPT = """/usr/bin/osascript<<END
        #        tell application "Finder" to
        #        set desktop picture to POSIX file "%s"
        #        end tell
        #        END"""
        #        subprocess.Popen(SCRIPT%wallpaper_path, shell=True)
        else:
            if (
                first_run
            ):  # don't spam the user with the same message over and over again
                sys.stderr.write(
                    "Warning: Failed to set wallpaper. Your desktop environment is not supported."
                )
                sys.stderr.write(
                    "You can try manually to set Your wallpaper to %s" % wallpaper_path
                )
            return False
        if first_run:
            first_run = False
        return True
    except:
        sys.stderr.write("ERROR: Failed to set wallpaper. There might be a bug.\n")
        return False


def _get_config_dir(app_name: str):
    if "XDG_CONFIG_HOME" in os.environ:
        confighome = os.environ["XDG_CONFIG_HOME"]
    elif "APPDATA" in os.environ:  # On Windows
        confighome = os.environ["APPDATA"]
    else:
        confighome = os.environ.get("XDG_HOMD_CONFIG", os.path.expanduser(".config"))
    configdir = os.path.join(confighome, app_name)
    return configdir


# Source(geekpradd): PyWallpapyer https://github.com/geekpradd/PyWallpaper/blob/cc69a2784109d27100c3ecabb336e5bba8a1d923/PyWallpaper.py#L17
def get_output(command):
    p = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    out, _ = p.communicate()
    return out


# Source(Martin Hansen, Serge Stroobandt): https://stackoverflow.com/a/21213358
def _get_desktop_environment():
    # From http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=1139057
    if sys.platform in ["win32", "cygwin"]:
        return "windows"
    elif sys.platform == "darwin":
        return "mac"
    else:  # Most likely either a POSIX system or something not much common
        desktop_session = os.environ.get("DESKTOP_SESSION")
        if (
            desktop_session is not None
        ):  # easier to match if we doesn't have  to deal with caracter cases
            desktop_session = desktop_session.lower()
            if desktop_session in [
                "gnome",
                "unity",
                "cinnamon",
                "mate",
                "xfce4",
                "lxde",
                "fluxbox",
                "blackbox",
                "openbox",
                "icewm",
                "jwm",
                "afterstep",
                "trinity",
                "kde",
            ]:
                return desktop_session
            ## Special cases ##
            # Canonical sets $DESKTOP_SESSION to Lubuntu rather than LXDE if using LXDE.
            # There is no guarantee that they will not do the same with the other desktop environments.
            elif "xfce" in desktop_session or desktop_session.startswith("xubuntu"):
                return "xfce4"
            elif desktop_session.startswith("ubuntustudio"):
                return "kde"
            elif desktop_session.startswith("ubuntu"):
                return "gnome"
            elif desktop_session.startswith("lubuntu"):
                return "lxde"
            elif desktop_session.startswith("kubuntu"):
                return "kde"
            elif desktop_session.startswith("razor"):  # e.g. razorkwin
                return "razor-qt"
            elif desktop_session.startswith("wmaker"):  # e.g. wmaker-common
                return "windowmaker"
            elif desktop_session.startswith("pop"):  # e.g. wmaker-common
                return "gnome"
        if os.environ.get("KDE_FULL_SESSION") == "true":
            return "kde"
        elif os.environ.get("GNOME_DESKTOP_SESSION_ID"):
            if not "deprecated" in os.environ.get("GNOME_DESKTOP_SESSION_ID"):  # type: ignore
                return "gnome2"
        # From http://ubuntuforums.org/showthread.php?t=652320
        elif _is_running("xfce-mcs-manage"):
            return "xfce4"
        elif _is_running("ksmserver"):
            return "kde"
    return "unknown"


def _is_running(process):
    # From http://www.bloggerpolis.com/2011/05/how-to-check-if-a-process-is-running-using-python/
    # and http://richarddingwall.name/2009/06/18/windows-equivalents-of-ps-and-kill-commands/
    try:  # Linux/Unix
        s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
    except:  # Windows
        s = subprocess.Popen(["tasklist", "/v"], stdout=subprocess.PIPE)

    if s.stdout:
        for x in s.stdout:
            if re.search(process, x):
                return True
    return False


def does_desktop_shortcut_exists(name: str):
    file = Path(name)
    return Path(
        os.path.expanduser("~/Desktop") / file.with_name(f"{file.name}.desktop")
    ).exists()


def make_shortcut(
    path: Path,
    icon: Path | str,
    script_or_command: str | list[str],
    title: str | None = None,
    file_name: str | None = None,
) -> bool:
    if title is None:
        if isinstance(script_or_command, str):
            title = script_or_command
        elif isinstance(icon, str):
            title = icon
        else:
            title = icon.name.replace("_icon", "")

    if isinstance(icon, str):
        icon = path / "default_assets" / f"{icon}_icon.ico"

    if file_name is None:
        file_name = title.lower()

    if isinstance(script_or_command, str):
        script_path = str((path / f"{script_or_command}").absolute())
        script_or_command = [sys.executable, script_path]

    shortcut_content = f"""[Desktop Entry]
    Version=1.0
    Name={title}
    Exec={shlex.join(script_or_command)}
    Icon={str(icon.absolute())}
    Terminal=false
    Type=Application
    Categories=Application;
    """

    file_name = f"{file_name}.desktop"
    desktop_file = Path(os.path.expanduser("~/Desktop")) / file_name
    try:
        desktop_file.write_text(shortcut_content)
        if _get_desktop_environment() == "gnome":
            subprocess.run(
                [
                    "gio",
                    "set",
                    str(desktop_file.absolute()),
                    "metadata::trusted",
                    "true",
                ]
            )
    except:
        return False
    return True


# FIXME: Shouldn't be started with profile as it is not made to launch GUI application.
# Another problem is that VSCODE run .profile, and so run edgeware on start. Tempfix
def toggle_run_at_startup(path: Path, state: bool):
    command = f"{sys.executable} {str((path / 'start.pyw').absolute())}&"

    edgeware_content = f"""############## EDGEWARE ##############
if [[ ! "${{GIO_LAUNCHED_DESKTOP_FILE}}" == "/usr/share/applications/code.desktop" ]] && [[ ! "${{TERM_PROGRAM}}" == "vscode" ]]; then
    {command}
fi
############## EDGEWARE ##############
"""

    edgeware_profile = Path(os.path.expanduser("~/.profile"))

    profile = edgeware_profile.read_text()
    edgeware_profile.with_name(".profile_ew_backup").write_text(profile)

    if state:
        profile += edgeware_content
    else:
        profile = profile.replace(edgeware_content, "")
    edgeware_profile.write_text(profile)
