import os, random as rand, tkinter as tk, threading as thread, time, json
from tkinter import *
from tkinter import messagebox
from itertools import count, cycle
from PIL import Image, ImageTk

allow_scream = False
with open(os.path.abspath(os.getcwd()) + '\\config.cfg', 'r') as cfg:
    jsonObj = json.loads(cfg.read())
    allow_scream = int(jsonObj['promptMod']) > 0

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
    arr = os.listdir(os.path.abspath(os.getcwd()) + '\\resource\\img\\')
    item = arr[rand.randrange(len(arr))]
    image = Image.open(os.path.abspath(os.getcwd()) + '\\resource\\img\\' + item)

    gif_bool = item.split('.')[len(item.split('.')) - 1].lower() == 'gif'
    windowObj = Tk()
    windowObj.configure(bg='black')
    canv = Canvas(windowObj, bg='black')
    scalefactor = float(rand.randint(20, 28)) / 100.0
    newWid = int((image.width * (float(windowObj.winfo_screenwidth()) / float(image.width)) * scalefactor))
    newHgt = int((image.height * (float(windowObj.winfo_screenwidth()) / float(image.width))* scalefactor))
    image_ = ImageTk.PhotoImage(image.resize((newWid, newHgt), Image.ANTIALIAS))
    if(not gif_bool):
        label = Label(canv, image=image_, bg='black')
        label.grid(row=0, column=0)
    else:
        label = GImg(windowObj)
        label.load(path=os.path.abspath(os.getcwd()) + '\\resource\\img\\' + item)
        label.pack()

    locX = rand.randint(0, max(windowObj.winfo_screenwidth() - (label.winfo_reqwidth() if not gif_bool else image.width + 50), 0))
    locY = rand.randint(0, max(windowObj.winfo_screenheight() - (label.winfo_reqheight() if not gif_bool else image.height + 50), 0))
    windowObj.geometry('%dx%d+%d+%d' % ((newWid if not gif_bool else image.width), (newHgt if not gif_bool else image.height), locX, locY))
    
    if(gif_bool):
        label.nextFrame()

    windowObj.overrideredirect(1)
    windowObj.frame = Frame(windowObj, borderwidth=2, relief=RAISED)
    windowObj.wm_attributes('-topmost', 1)
    subButton = Button(windowObj, text='I Submit <3', command=die)
    subButton.place(x=label.winfo_reqwidth() - 5 - subButton.winfo_reqwidth(), y=label.winfo_reqheight() - 5 - subButton.winfo_reqheight())
    canv.pack()
    if allow_scream:
        thread.Thread(target=lambda: scream(windowObj)).start()
    windowObj.mainloop()

def scream(root):
    while True:
        time.sleep(rand.randint(1, 3))
        root.focus_force()

def die():
    os.kill(os.getpid(), 9)

try:
    unborderedWindow()
except:
    messagebox.showerror('Popup Error', 'Could not show popup, usually due to Pillow not being installed or because of an unknown image type in the /img/ folder. Please either update to the latest version or install Pillow using PIP in order to use Edgeware.')