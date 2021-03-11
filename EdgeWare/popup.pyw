import os
import random as rand
import tkinter as tk

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

class WImg: 
    def __init__(self, scalefactor , wid):
        arr = os.listdir(os.path.abspath(os.getcwd()) + '\\resource\\img\\')
        item = arr[rand.randrange(len(arr))]
        image = Image.open(os.path.abspath(os.getcwd()) + '\\resource\\img\\' + item)
        newWid = int((image.width * (float(wid) / float(image.width)) * scalefactor))
        newHgt = int((image.height * (float(wid) / float(image.width))* scalefactor))
        self.image = ImageTk.PhotoImage(image.resize((newWid, newHgt), Image.ANTIALIAS))

    def get(self):
        return self.image

def unborderedWindow():
    windowObj = Tk()
    img = WImg(float(rand.randint(20, 28)) / 100.0, windowObj.winfo_screenwidth()).get()
    label = tk.Label(windowObj, image=img)
    label.columnconfigure(0, weight=1)
    label.rowconfigure(0, weight=1)
    label.grid(row=0, column=0)

    locX = rand.randint(0, max(windowObj.winfo_screenwidth() - label.winfo_reqwidth(), 0))
    locY = rand.randint(0, max(windowObj.winfo_screenheight() - label.winfo_reqheight(), 0))
    windowObj.geometry('%dx%d+%d+%d' % (label.winfo_reqwidth(), label.winfo_reqheight(), locX, locY))

    windowObj.overrideredirect(1)
    windowObj.frame = Frame(windowObj, borderwidth=2, relief=RAISED)
    windowObj.frame.pack_propagate(True)
    windowObj.wm_attributes('-topmost', 1)
    subButton = Button(windowObj, text='I Submit <3', command=die)
    subButton.place(x=label.winfo_reqwidth() - 5 - subButton.winfo_reqwidth(), y=label.winfo_reqheight() - 5 - subButton.winfo_reqheight())
    windowObj.mainloop()

def die():
    os.kill(os.getpid(), 9)

try:
    unborderedWindow()
except:
    messagebox.showerror('Popup Error', 'Could not show popup, usually due to Pillow not being installed or because of an unknown image type in the /img/ folder. Please either update to the latest version or install Pillow using PIP in order to use Edgeware.')