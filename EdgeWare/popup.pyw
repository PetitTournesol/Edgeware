import os, random as rand, tkinter as tk, threading as thread, time, json, ctypes, pathlib
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
panic_key = ''
captions = json.loads('{}')
PATH = str(pathlib.Path(__file__).parent.absolute())

with open(PATH + '\\config.cfg', 'r') as cfg:
    jsonObj = json.loads(cfg.read())
    show_captions = int(jsonObj['showCaptions']) == 1
    allow_scream = int(jsonObj['promptMod']) == 0
    panic_disabled = int(jsonObj['panicDisabled']) == 1
    panic_key = jsonObj['panicButton']

try:
    with open(PATH + '\\resource\\captions.json', 'r') as capF:
        captions = json.loads(capF.read())
    has_captions = True
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
    scalefactor = float(rand.randint(25, 28)) / 100.0
    border_wid_const = 5
    monitor_data = monitor_areas()

    aspect_WH = image.width / image.height
    aspect_HW = image.height / image.width
    ogSize = image.width*image.height

    data_list = list(monitor_data[rand.randrange(0, len(monitor_data))][2])
    screenWid = data_list[2]-data_list[0]
    screenHgt = data_list[3] - data_list[1]

    #window start
    root = Tk()
    root.bind('<KeyPress>', lambda key: panic(key))
    root.configure(bg='black')
    root.overrideredirect(1)
    root.frame = Frame(root, borderwidth=border_wid_const, relief=RAISED)
    root.wm_attributes('-topmost', 1)

    #super ugly method of downscaling, but I'm an idiot so as long as it works, I don't really care
        #scalefactor uses scaling of 40-55% if image is > 640000 pixels, otherwises scales by 80-110% scaling applied
        #   this is to ensure that already small images are not downsized by a large amount
    scalefactor = float(rand.randint(40, 55)) / 100.0 if ogSize > (800*800) else float(rand.randint(80, 110)) / 100.0
        #calculates new width&height from the minimum aspect ratio between width/height and height/width, then takes the
        #   minimum between the new formula and the old
    newWid = min(int(image.width*min(aspect_WH, aspect_HW)*scalefactor), int((image.width * (float(screenWid) / float(image.width)) * scalefactor)))
    newHgt = min(int(image.height*min(aspect_WH, aspect_HW)*scalefactor), int((image.height * (float(screenWid) / float(image.width))* scalefactor)))
    rImg = image.resize((newWid - border_wid_const+1, newHgt - border_wid_const+1), Image.ANTIALIAS)
        #could potentially get stuck with ungodly massive images, but just don't use 500x10e50 dim images
        #   if image is STILL too large for screen after above changes, forcibly downscales it by 75% repeatedly until it fits
    while(rImg.height > screenHgt or rImg.width > screenWid):
        rImg = rImg.resize((int(rImg.width*0.75), int(rImg.height*0.75)), Image.ANTIALIAS)
        newWid = int(newWid*0.75)
        newHgt = int(newHgt*0.75)

    image_ = ImageTk.PhotoImage(rImg)
    
    #different handling for gifs vs normal images
    if(not gif_bool):
        label = Label(root, image=image_, bg='black')
        label.grid(row=0, column=0)
    else:
        label = GImg(root)
        label.load(path=os.path.abspath(os.getcwd()) + '\\resource\\img\\' + item, rWid = newWid, rHgt = newHgt)
        label.pack()

    locX = rand.randint(data_list[0], data_list[2] - (newWid + 50))
    locY = rand.randint(data_list[1], max(data_list[3] - (newHgt + 50), 0))

    root.geometry('%dx%d+%d+%d' % ((rImg.width), (rImg.height), locX, locY))
    
    if(gif_bool):
        label.nextFrame()

    if show_captions and has_captions:
        captionLabel = Label(root, text=selectCaption(item), wraplength=label.winfo_reqwidth() - border_wid_const - 10)
        captionLabel.place(x=5, y=5)
    subButton = Button(root, text='I Submit <3', command=die)
    subButton.place(x=newWid - 5 - subButton.winfo_reqwidth(), y=newHgt - 5 - subButton.winfo_reqheight())
    #disabled for performance
    #if allow_scream:
    #    thread.Thread(target=lambda: scream(root)).start()
    root.mainloop()

def scream(root):
    while True:
        time.sleep(rand.randint(1, 3))
        root.focus_force()

def die():
    os.kill(os.getpid(), 9)

def selectCaption(strObj):
    for obj in captions['prefix']:
        if strObj.startswith(obj):
            return captions[obj][rand.randrange(0, len(captions[obj]))]
    return captions['default'][rand.randrange(0, len(captions['default']))]

def panic(key):
    if not panic_disabled and key.keycode == panic_key:
        os.startfile('panic.pyw')

#try:
unborderedWindow()
#except Exception as e:
#    messagebox.showerror('Popup Error', 'Could not show popup, usually due to Pillow not being installed or because of an unknown image type in the /img/ folder. Please either update to the latest version or install Pillow using PIP in order to use Edgeware.\n[' + str(e) + ']')