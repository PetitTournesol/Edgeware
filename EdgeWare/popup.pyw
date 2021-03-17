import os, random as rand, tkinter as tk, threading as thread, time, json
from tkinter import *
from tkinter import messagebox
from itertools import count, cycle
from PIL import Image, ImageTk

#TODO: FIX SCALING AGAIN

allow_scream = True
show_captions = False
has_captions = False
panic_disabled = False
panic_key = ''
captions = json.loads('{}')
PATH = os.path.abspath(os.getcwd())

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
    def load(self, path, delay=75):
        self.image = Image.open(path)
        self.frames = []
        self.delay = delay
        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(self.image.copy()))
                self.image.seek(i)
        except:
            print('Done register frames.')
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

    #window start
    root = Tk()
    root.bind('<KeyPress>', lambda key: panic(key))
    root.configure(bg='black')
    root.overrideredirect(1)
    root.frame = Frame(root, borderwidth=border_wid_const, relief=RAISED)
    root.wm_attributes('-topmost', 1)
    canv = Canvas(root, bg='black')
    
    screenWid = root.winfo_screenwidth()
    screenHgt = root.winfo_screenheight()

    scalefactor = float(rand.randint(20, 28)) / 100.0
    newWid = int((image.width * (float(screenWid) / float(image.width)) * scalefactor))
    newHgt = int((image.height * (float(screenWid) / float(image.width))* scalefactor))
    image_ = ImageTk.PhotoImage(image.resize((newWid - border_wid_const+1, newHgt - border_wid_const+1), Image.ANTIALIAS))

    #different handling for gifs vs other images
    if(not gif_bool):
        label = Label(canv, image=image_, bg='black')
        label.grid(row=0, column=0)
    else:
        label = GImg(root)
        label.load(path=os.path.abspath(os.getcwd()) + '\\resource\\img\\' + item)
        label.pack()

    locX = rand.randint(0, max(screenWid - (label.winfo_reqwidth() if not gif_bool else image.width + 50), 0))
    locY = rand.randint(0, max(screenHgt - (label.winfo_reqheight() if not gif_bool else image.height + 50), 0))
    root.geometry('%dx%d+%d+%d' % ((newWid if not gif_bool else image.width), (newHgt if not gif_bool else image.height), locX, locY))
    
    if(gif_bool):
        label.nextFrame()

    if show_captions and has_captions:
        captionLabel = Label(root, text=selectCaption(item), wraplength=label.winfo_reqwidth() - border_wid_const - 10)
        captionLabel.place(x=5, y=5)
    subButton = Button(root, text='I Submit <3', command=die)
    subButton.place(x=label.winfo_reqwidth() - 5 - subButton.winfo_reqwidth(), y=label.winfo_reqheight() - 5 - subButton.winfo_reqheight())
    canv.pack()
    if allow_scream:
        thread.Thread(target=lambda: scream(root)).start()
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
    print(key.keycode)
    print(panic_key)
    if not panic_disabled and key.keycode == panic_key:
        os.startfile('panic.pyw')

try:
    unborderedWindow()
except Exception as e:
    messagebox.showerror('Popup Error', 'Could not show popup, usually due to Pillow not being installed or because of an unknown image type in the /img/ folder. Please either update to the latest version or install Pillow using PIP in order to use Edgeware.\n[' + str(e) + ']')