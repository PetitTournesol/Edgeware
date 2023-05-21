import ctypes
from ctypes import util
import hashlib
import json
import logging
import os
import pathlib
import random as rand
import subprocess
import sys
import threading as thread
import time
import tkinter as tk
import webbrowser
from itertools import count, cycle
from tkinter import RAISED, Button, Frame, Label, Tk, messagebox, simpledialog
from PIL import Image, ImageFilter, ImageTk
from utils import utils

SYS_ARGS = sys.argv.copy()
SYS_ARGS.pop(0)


class RECT(ctypes.Structure):  # rect class for containing monitor info
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]

    def dump(self):
        return map(int, (self.left, self.top, self.right, self.bottom))


# End Imported Code

# used to check passed tags for script mode
def checkTag(tag) -> bool:
    return [c.startswith(tag) for c in SYS_ARGS].count(True) >= 1


def check_setting(name: str, default: bool = False) -> bool:
    default = False if default is None else default
    try:
        return int(settings.get(name)) == 1
    except:
        return default


PATH = pathlib.Path(__file__).parent
os.chdir(PATH)

config_file = PATH / "config.cfg"

ALLOW_SCREAM = True
SHOW_CAPTIONS = False
PANIC_DISABLED = False
EXTREME_MODE = False
WEB_OPEN = False
HAS_LIFESPAN = False
LIFESPAN = 0
WEB_PROB = 0
MITOSIS_STRENGTH = 2
SUBMISSION_TEXT = "I Submit <3"
PANIC_KEY = ""
PANIC_REQUIRES_VALIDATION = False
HASHED_PATH = None
CAPTIONS = {}
LOWKEY_MODE = False
LOWKEY_CORNER = 0
DELAY = 0
OPACITY = 100
VIDEO_VOLUME = 0.25
FADE_OUT_TIME = 1.5
DENIAL_MODE = False
DENIAL_CHANCE = 0
SUBLIMINAL_MODE = False

config_file = PATH / "config.cfg"
settings = json.loads(config_file.read_text())

SHOW_CAPTIONS = check_setting("showCaptions")
PANIC_DISABLED = check_setting("panicDisabled")
MITOSIS_MODE = check_setting("mitosisMode")
WEB_OPEN = check_setting("webPopup")
WEB_PROB = int(settings["webMod"])
PANIC_KEY = settings["panicButton"]
HAS_LIFESPAN = check_setting("timeoutPopups")
LIFESPAN = int(settings["popupTimeout"])
MITOSIS_STRENGTH = int(settings["mitosisStrength"])
PANIC_REQUIRES_VALIDATION = check_setting("timerMode")
LOWKEY_MODE = check_setting("lkToggle")
LOWKEY_CORNER = int(settings["lkCorner"])
DELAY = int(settings["delay"])
OPACITY = int(settings["lkScaling"])

VIDEO_VOLUME = float(settings["videoVolume"]) / 100
VIDEO_VOLUME = min(max(0, VIDEO_VOLUME), 1)

DENIAL_MODE = check_setting("denialMode")
DENIAL_CHANCE = int(settings["denialChance"])
SUBLIMINAL_MODE = check_setting("popupSubliminals")

# functions for script mode, unused for now
if checkTag("timeout="):
    HAS_LIFESPAN = True
    LIFESPAN = int(
        SYS_ARGS[[c.startswith("timeout=") for c in SYS_ARGS].index(True)].split("=")[1]
    )

if checkTag("mitosis="):
    MITOSIS_MODE = True
    MITOSIS_STRENGTH = int(
        SYS_ARGS[[c.startswith("mitosis=") for c in SYS_ARGS].index(True)].split("=")[1]
    )

if checkTag("hideCap"):
    SHOW_CAPTIONS = False

if checkTag("showCap"):
    SHOW_CAPTIONS = True
# end script mode function tag checks

# used for timer mode, checks if password is required to panic
if PANIC_REQUIRES_VALIDATION:
    hash_file = PATH / "pass.hash"
    try:
        HASHED_PATH = hash_file.read_text()
    except:
        # no hash found
        HASHED_PATH = None

if WEB_OPEN:
    web_dict = ""
    web_resource = PATH / "resource" / "web.json"
    if web_resource.exists():
        web_dict = json.loads(web_resource.read_text())


caption_file = PATH / "resource" / "captions.json"
if caption_file.exists():
    CAPTIONS = json.loads(caption_file.read_text())
    try:
        SUBMISSION_TEXT = CAPTIONS["subtext"]
    except:
        print("will use default submission text")
else:
    print("no CAPTIONS.json")


# gif label class
class GifLabel(tk.Label):
    def load(
        self,
        path: str,
        resized_width: int,
        resized_height: int,
        delay: int = 75,
        back_image: Image.Image = None,
    ):
        self.image = Image.open(path)
        self.configure(background="black")
        self.frames: list[ImageTk.PhotoImage] = []
        self.delay = delay
        try:
            for i in count(1):
                hold_image = self.image.resize(
                    (resized_width, resized_height), Image.BOX
                )
                if back_image is not None:
                    hold_image, back_image = hold_image.convert(
                        "RGBA"
                    ), back_image.convert("RGBA")
                    hold_image = Image.blend(back_image, hold_image, 0.2)
                self.frames.append(ImageTk.PhotoImage(hold_image.copy()))
                self.image.seek(i)
        except Exception as e:
            print(f"{e}")
            print(f"Done register frames. ({len(self.frames)})")
        self.frames_ = cycle(self.frames)

    def next_frame(self):
        if self.frames_:
            self.config(image=next(self.frames_))
            self.after(self.delay, self.next_frame)


# video label class
class VideoLabel(tk.Label):
    def load(self, path: str, resized_width: int, resized_height: int):
        import imageio
        from moviepy.editor import AudioFileClip
        from videoprops import get_video_properties

        self.path = path
        self.configure(background="black")
        self.wid = resized_width
        self.hgt = resized_height
        self.video_properties = get_video_properties(path)
        self.audio = AudioFileClip(self.path)
        self.fps = float(self.video_properties["avg_frame_rate"].split("/")[0]) / float(
            self.video_properties["avg_frame_rate"].split("/")[1]
        )
        try:
            self.audio_track = self.audio.to_soundarray()
            print(self.audio_track)
            self.audio_track = [
                [VIDEO_VOLUME * v[0], VIDEO_VOLUME * v[1]] for v in self.audio_track
            ]
            self.duration = float(self.video_properties["duration"])
        except:
            self.audio_track = None
            self.duration = None
        self.video_frames = imageio.get_reader(path)
        self.delay = 1 / self.fps

    def play(self):
        from types import NoneType

        if not isinstance(self.audio_track, NoneType):
            try:
                import sounddevice

                sounddevice.play(
                    self.audio_track,
                    samplerate=len(self.audio_track) / self.duration,
                    loop=True,
                )
            except Exception as e:
                print(f"failed to play sound, reason:\n\t{e}")
        while True:
            for frame in self.video_frames.iter_data():
                self.time_offset_start = time.perf_counter()
                self.video_frame_image = ImageTk.PhotoImage(
                    Image.fromarray(frame).resize((self.wid, self.hgt))
                )
                self.config(image=self.video_frame_image)
                self.image = self.video_frame_image
                self.time_offset_end = time.perf_counter()
                time.sleep(
                    max(0, self.delay - (self.time_offset_end - self.time_offset_start))
                )


def run():
    # var things
    arr = os.listdir(PATH / "resource" / "img")
    item = arr[rand.randrange(len(arr))]
    video_mode = False

    while item.split(".")[-1].lower() == "ini":
        item = arr[rand.randrange(len(arr))]

    if len(SYS_ARGS) >= 1 and SYS_ARGS[0] != "%RAND%":
        item = rand.choice(os.listdir(PATH / "resource" / "vid"))

    if len(SYS_ARGS) >= 1 and SYS_ARGS[0] == "-video":
        video_mode = True

    if not video_mode:
        while True:
            try:
                image = Image.open(PATH / "resource" / "img" / item)
                break
            except:
                item = rand.choice(arr)
    else:
        from videoprops import get_video_properties

        video_path = PATH / "resource" / "vid" / item
        video_properties = get_video_properties(video_path)
        image = Image.new(
            "RGB", (video_properties["width"], video_properties["height"])
        )

    gif_bool = item.split(".")[-1].lower() == "gif"
    border_wid_const = 5
    monitor_data = utils.monitor_areas()

    area = rand.choice(monitor_data)

    # window start
    root = Tk()
    root.bind("<KeyPress>", lambda key: panic(key))
    root.configure(bg="black")
    root.overrideredirect(1)
    root.frame = Frame(root)
    root.wm_attributes("-topmost", 1)

    # many thanks to @MercyNudes for fixing my old braindead scaling method (https://twitter.com/MercyNudes)
    def resize(img: Image.Image) -> Image.Image:
        size_source = max(img.width, img.height) / min(area.width, area.height)
        size_target = (
            rand.randint(30, 70) / 100
            if not LOWKEY_MODE
            else rand.randint(20, 50) / 100
        )
        resize_factor = size_target / size_source
        return image.resize(
            (int(image.width * resize_factor), int(image.height * resize_factor)),
            Image.ANTIALIAS,
        )

    resized_image = resize(image)

    do_deny = check_deny()

    if do_deny and not gif_bool:
        blur_modes = [
            ImageFilter.GaussianBlur(5),
            ImageFilter.GaussianBlur(10),
            ImageFilter.GaussianBlur(20),
            ImageFilter.BoxBlur(5),
            ImageFilter.BoxBlur(10),
            ImageFilter.BoxBlur(20),
        ]
        rand.shuffle(blur_modes)
        resized_image = resized_image.filter(blur_modes.pop())

    photoimage_image = ImageTk.PhotoImage(resized_image)
    image.close()

    # different handling for videos vs gifs vs normal images
    if video_mode:
        # video mode
        label = VideoLabel(root)
        label.load(
            path=str(video_path.absolute()),
            resized_width=resized_image.width,
            resized_height=resized_image.height,
        )
        label.pack()
        thread.Thread(target=lambda: label.play(), daemon=True).start()
    elif gif_bool:
        # gif mode
        label = GifLabel(root)
        label.load(
            path=str((PATH / "resource" / "img" / item).absolute()),
            resized_width=resized_image.width,
            resized_height=resized_image.height,
        )
        label.pack()
    else:
        # standard image mode
        if not SUBLIMINAL_MODE:
            label = Label(root, image=photoimage_image, bg="black")
            label.pack()
        else:
            label = GifLabel(root)
            subliminal_path = PATH / "default_assets" / "default_spiral.gif"

            subliminals = PATH / "resources" / "subliminals"
            if subliminals.exists():
                subliminal_options = [
                    file
                    for file in os.listdir(subliminals)
                    if file.lower().endswith(".gif")
                ]
                if len(subliminal_options) > 0:
                    subliminal_path = subliminals / rand.choice(subliminal_options)

            label.load(
                subliminal_path,
                photoimage_image.width(),
                photoimage_image.height(),
                back_image=resized_image,
            )
            label.pack()
            label.next_frame()

        if do_deny:
            deny_options = CAPTIONS.get("denial")
            if deny_options is None or len(CAPTIONS["denial"]) == 0:
                deny_text = "Not for you~"
            else:
                rand.shuffle(CAPTIONS["denial"])
                deny_text = CAPTIONS["denial"].pop()
            denyLabel = Label(label, text=deny_text)
            denyLabel.place(
                x=int(resized_image.width / 2) - int(denyLabel.winfo_reqwidth() / 2),
                y=int(resized_image.height / 2) - int(denyLabel.winfo_reqheight() / 2),
            )

    locX = rand.randint(area.x, area.width - (resized_image.width))
    locY = rand.randint(area.y, max(area.height - (resized_image.height), 0))

    if LOWKEY_MODE:
        global LOWKEY_CORNER
        if LOWKEY_CORNER == 4:
            LOWKEY_CORNER = rand.randrange(0, 3)
        if LOWKEY_CORNER == 0:
            locX = area.width - (resized_image.width)
            locY = 0
        elif LOWKEY_CORNER == 1:
            locX = 0
            locY = 0
        elif LOWKEY_CORNER == 2:
            locX = 0
            locY = area.height - (resized_image.height)
        elif LOWKEY_CORNER == 3:
            locX = area.width - (resized_image.width)
            locY = area.height - (resized_image.height)

    root.geometry(
        f"{resized_image.width + border_wid_const - 1}x{resized_image.height + border_wid_const - 1}+{locX}+{locY}"
    )

    if gif_bool:
        label.next_frame()

    if HAS_LIFESPAN or LOWKEY_MODE:
        thread.Thread(
            target=lambda: live_life(
                root, LIFESPAN if not LOWKEY_MODE else DELAY / 1000
            ),
            daemon=True,
        ).start()

    if SHOW_CAPTIONS and CAPTIONS:
        caption_text = select_caption(item)
        if caption_text is not None:
            captionLabel = Label(
                root,
                text=caption_text,
                wraplength=resized_image.width - border_wid_const,
            )
            captionLabel.place(x=5, y=5)

    submit_button = Button(root, text=SUBMISSION_TEXT, command=die)
    submit_button.place(
        x=resized_image.width - 5 - submit_button.winfo_reqwidth(),
        y=resized_image.height - 5 - submit_button.winfo_reqheight(),
    )

    root.attributes("-alpha", OPACITY / 100)
    root.mainloop()


def check_deny() -> bool:
    return DENIAL_MODE and rand.randint(1, 100) <= DENIAL_CHANCE


def live_life(parent: tk, length: int):
    time.sleep(length)
    for i in range(100 - OPACITY, 100):
        parent.attributes("-alpha", 1 - i / 100)
        time.sleep(FADE_OUT_TIME / 100)
    if LOWKEY_MODE:
        utils.run_popup_script()
    os.kill(os.getpid(), 9)


def do_roll(mod: int):
    return mod > rand.randint(0, 100)


def select_url(arg: str):
    return (
        web_dict["urls"][arg]
        + web_dict["args"][arg].split(",")[
            rand.randrange(len(web_dict["args"][arg].split(",")))
        ]
    )


def die():
    if WEB_OPEN and web_dict and do_roll((100 - WEB_PROB) / 2) and not LOWKEY_MODE:
        urlPath = select_url(rand.randrange(len(web_dict["urls"])))
        webbrowser.open_new(urlPath)
    if MITOSIS_MODE or LOWKEY_MODE:
        for _ in range(0, MITOSIS_STRENGTH) if not LOWKEY_MODE else [1]:
            utils.run_popup_script()
    os.kill(os.getpid(), 9)


def select_caption(filename: str) -> str:
    for obj in CAPTIONS["prefix"]:
        if filename.startswith(obj):
            ls = CAPTIONS[obj]
            ls.extend(CAPTIONS["default"])
            return ls[rand.randrange(0, len(CAPTIONS[obj]))]
    return (
        CAPTIONS["default"][rand.randrange(0, len(CAPTIONS["default"]))]
        if (len(CAPTIONS["default"]) > 0)
        else None
    )


def panic(key):
    key_condition = key.keysym == PANIC_KEY or key.keycode == PANIC_KEY
    if PANIC_REQUIRES_VALIDATION and key_condition:
        try:
            hash_file_path = PATH / "pass.hash"
            time_file_path = PATH / "hid_time.dat"
            pass_ = simpledialog.askstring("Panic", "Enter Panic Password")
            t_hash = (
                None
                if pass_ == None or pass_ == ""
                else hashlib.sha256(
                    pass_.encode(encoding="ascii", errors="ignore")
                ).hexdigest()
            )
            if t_hash == HASHED_PATH:
                # revealing hidden files
                try:
                    utils.expose_file(hash_file_path)
                    utils.expose_file(time_file_path)
                    os.remove(hash_file_path)
                    os.remove(time_file_path)
                    utils.run_panic_script()
                except:
                    # if some issue occurs with the hash or time files just emergency panic
                    utils.run_panic_script()
        except:
            # if some issue occurs with the hash or time files just emergency panic
            utils.run_panic_script()
    else:
        if not PANIC_DISABLED and key_condition:
            utils.run_panic_script()


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        if not os.path.exists(os.path.join(PATH, "logs")):
            os.mkdir(os.path.join(PATH, "logs"))
        logging.basicConfig(
            filename=os.path.join(
                PATH,
                "logs",
                time.asctime().replace(" ", "_").replace(":", "-") + "-popup.txt",
            ),
            format="%(levelname)s:%(message)s",
            level=logging.DEBUG,
        )
        logging.fatal(f"failed to start popup\n{e}")
