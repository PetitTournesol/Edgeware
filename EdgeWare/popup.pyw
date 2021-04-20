import os, random as rand, tkinter as tk, time, json, pathlib, webbrowser, ctypes, threading as thread
from tkinter import *
from tkinter import messagebox
from itertools import count, cycle
from PIL import Image, ImageTk

#Start Imported Code
#Code from: https://code.activestate.com/recipes/460509-get-the-actual-and-usable-sizes-of-all-the-monitor/
user = ctypes.windll.user32

class RECT(ctypes.Structure): #rect class for containing monitor info
    _fields_ = [
        ('left', ctypes.c_long),
        ('top', ctypes.c_long),
        ('right', ctypes.c_long),
        ('bottom', ctypes.c_long)
        ]
    def dump(self):
        return map(int, (self.left, self.top, self.right, self.bottom))

class MONITORINFO(ctypes.Structure): #unneeded for this, but i don't want to rework the entire thing because i'm stupid
    _fields_ = [
        ('cbSize', ctypes.c_ulong),
        ('rcMonitor', RECT),
        ('rcWork', RECT),
        ('dwFlags', ctypes.c_ulong)
        ]

def get_monitors():
    retval = []
    CBFUNC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(RECT), ctypes.c_double)
    def cb(hMonitor, hdcMonitor, lprcMonitor, dwData):
        r = lprcMonitor.contents
        data = [hMonitor]
        data.append(r.dump())
        retval.append(data)
        return 1
    cbfunc = CBFUNC(cb)
    temp = user.EnumDisplayMonitors(0, 0, cbfunc, 0)
    return retval

def monitor_areas(): #all that matters from this is list(mapObj[monitor index][1])[k]; this is the list of monitor dimensions
    retval = []
    monitors = get_monitors()
    for hMonitor, extents in monitors:
        data = [hMonitor]
        mi = MONITORINFO()
        mi.cbSize = ctypes.sizeof(MONITORINFO)
        mi.rcMonitor = RECT()
        mi.rcWork = RECT()
        res = user.GetMonitorInfoA(hMonitor, ctypes.byref(mi))
        data.append(mi.rcMonitor.dump())
        data.append(mi.rcWork.dump())
        retval.append(data)
    return retval
#End Imported Code

allow_scream = True
show_captions = False
has_captions = False
panic_disabled = False
extreme_mode = False
web_open = False
has_lifespan = False
lifespan = 0
web_prob = 0
mitosis_stren = 2
submission_text = 'I Submit <3'
sqLim = 800
panic_key = ''
captions = json.loads('{}')
FADE_OUT_TIME = 1.5
PATH = str(pathlib.Path(__file__).parent.absolute())
os.chdir(PATH)

with open(PATH + '\\config.cfg', 'r') as cfg:
    jsonObj = json.loads(cfg.read())
    show_captions = int(jsonObj['showCaptions']) == 1
    allow_scream = int(jsonObj['promptMod']) == 0
    panic_disabled = int(jsonObj['panicDisabled']) == 1
    mitosis_enabled = int(jsonObj['mitosisMode']) == 1
    web_open = int(jsonObj['webPopup']) == 1
    web_prob = int(jsonObj['webMod'])
    sqLim = int(jsonObj['squareLim'])
    panic_key = jsonObj['panicButton']
    has_lifespan = int(jsonObj['timeoutPopups']) == 1
    if has_lifespan:
        lifespan = int(jsonObj['popupTimeout'])
    mitosis_stren = int(jsonObj['mitosisStrength'])
    #extreme_mode = int(jsonObj['extremeMode']) == 1

if web_open:
    webJsonDat = ''
    if os.path.exists(PATH + '\\resource\\web.json'):
        with open(PATH + '\\resource\\web.json', 'r') as webF:
            webJsonDat = json.loads(webF.read())
    hasWeb = len(webJsonDat['urls']) > 0

try:
    with open(PATH + '\\resource\\captions.json', 'r') as capF:
        captions = json.loads(capF.read())
        has_captions = True
        try:
            submission_text = captions['subtext']
        except:
            print('will use default submission text')
except:
    print('no captions.json')

class GImg(tk.Label):
    def load(self, path, rWid, rHgt, delay=75):
        self.image = Image.open(path)
        self.frames = []
        self.delay = delay
        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(self.image.resize((rWid, rHgt), Image.BOX).copy()))
                self.image.seek(i)
        except:
            print('Done register frames. (' + str(len(self.frames)) + ')')
        self.frames_ = cycle(self.frames)
    def nextFrame(self):
        if self.frames_:
            self.config(image=next(self.frames_))
            self.after(self.delay, self.nextFrame)

def unborderedWindow():
    #var things
    arr = os.listdir(os.path.abspath(os.getcwd()) + '\\resource\\img\\')
    item = arr[rand.randrange(len(arr))]
    while item.split('.')[len(item.split('.')) - 1].lower() == 'ini':
        item = arr[rand.randrange(len(arr))]
    image = Image.open(os.path.abspath(os.getcwd()) + '\\resource\\img\\' + item)
    gif_bool = item.split('.')[len(item.split('.')) - 1].lower() == 'gif'
    border_wid_const = 5
    monitor_data = monitor_areas()

    data_list = list(monitor_data[rand.randrange(0, len(monitor_data))][2])
    screenWid = data_list[2] - data_list[0]
    screenHgt = data_list[3] - data_list[1]

    #window start
    root = Tk()
    root.bind('<KeyPress>', lambda key: panic(key))
    root.configure(bg='black')
    root.overrideredirect(1)
    root.frame = Frame(root, borderwidth=border_wid_const, relief=RAISED)
    root.wm_attributes('-topmost', 1)

    #many thanks to @MercyNudes for fixing my old braindead scaling method (https://twitter.com/MercyNudes)
    def bResize(img) -> Image:
        size_source = max(img.width, img.height) / min(screenWid, screenHgt)
        size_target = rand.randint(30, 70) / 100
        resize_factor = size_target / size_source
        return image.resize((int(image.width * resize_factor), int(image.height * resize_factor)), Image.ANTIALIAS)
    
    image = bResize(image)
    
    while(image.height > screenHgt or image.width > screenWid):
        image = image.resize((int(image.width*0.75), int(image.height*0.75)), Image.ANTIALIAS)
    
    rImg = image #bResize(image)

    image_ = ImageTk.PhotoImage(rImg)
    
    #different handling for gifs vs normal images
    if(not gif_bool):
        label = Label(root, image=image_, bg='black')
        label.grid(row=0, column=0)
    else:
        label = GImg(root)
        label.load(path=os.path.abspath(os.getcwd()) + '\\resource\\img\\' + item, rWid = rImg.width, rHgt = rImg.height)
        label.pack()

    locX = rand.randint(data_list[0], data_list[2] - (rImg.width))
    locY = rand.randint(data_list[1], max(data_list[3] - (rImg.height), 0))

    root.geometry('%dx%d+%d+%d' % ((rImg.width), (rImg.height), locX, locY))
    
    if(gif_bool):
        label.nextFrame()
    
    if has_lifespan:
        thread.Thread(target=lambda: liveLife(root)).start()

    if show_captions and has_captions:
        capText = selectCaption(item)
        if len(capText) > 0:
            captionLabel = Label(root, text=capText, wraplength=rImg.width - border_wid_const)
            captionLabel.place(x=5, y=5)

    subButton = Button(root, text=submission_text, command=die)
    subButton.place(x=rImg.width - 5 - subButton.winfo_reqwidth(), y=rImg.height - 5 - subButton.winfo_reqheight())
    #disabled for performance
    #if allow_scream:
    #    thread.Thread(target=lambda: scream(root)).start()
    root.mainloop()

def liveLife(parent):
    time.sleep(lifespan)
    for i in range(0, 100):
        parent.attributes('-alpha', 1-i/100)
        time.sleep(FADE_OUT_TIME / 100)
    os.kill(os.getpid(), 9)

def doRoll(mod):
    return mod > rand.randint(0, 100)

def urlSelect(arg):
    return webJsonDat['urls'][arg] + webJsonDat['args'][arg].split(',')[rand.randrange(len(webJsonDat['args'][arg].split(',')))]

def scream(root):
    while True:
        time.sleep(rand.randint(1, 3))
        root.focus_force()

def die():
    if web_open and hasWeb and doRoll((100-web_prob) / 2):
        urlPath = urlSelect(rand.randrange(len(webJsonDat['urls'])))
        webbrowser.open_new(urlPath)
    if mitosis_enabled:
        for i in range(0, mitosis_stren):
            os.startfile('popup.pyw')
    os.kill(os.getpid(), 9)

def selectCaption(strObj):
    for obj in captions['prefix']:
        if strObj.startswith(obj):
            ls = captions[obj]
            ls.extend(captions['default'])
            return ls[rand.randrange(0, len(captions[obj]))]
    return captions['default'][rand.randrange(0, len(captions['default']))] if (len(captions['default']) > 0) else ''

def panic(key):
    if not panic_disabled and (key.keysym == panic_key or key.keycode == panic_key): #(post or is to keep backwards compatibility)
        os.startfile('panic.pyw')

try:
    unborderedWindow()
except Exception as e:
    messagebox.showerror('Popup Error', 'Could not show popup.\n[' + str(e) + ']')