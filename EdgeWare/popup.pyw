import os
import random as rand
import tkinter as tk

from win32api import GetSystemMetrics
from tkinter import *
from PIL import ImageTk, Image

class WImg: 
    def __init__(self, scalefactor):
        arr = os.listdir(os.path.abspath(os.getcwd()) + '\\resource\\img\\')
        image = Image.open(os.path.abspath(os.getcwd()) + '\\resource\\img\\' + arr[rand.randrange(len(arr))])
        newWid = int((image.width * (float(GetSystemMetrics(0)) / float(image.width)) * scalefactor))
        newHgt = int((image.height * (float(GetSystemMetrics(0)) / float(image.width))* scalefactor))
        self.image = ImageTk.PhotoImage(image.resize((newWid, newHgt), Image.ANTIALIAS))

    def get(self):
        return self.image

def unborderedWindow():
    windowObj = Tk()
    img = WImg(float(rand.randint(20, 28)) / 100.0).get()
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
    subButton = Button(windowObj, text='I Submit <3', command=exit)
    subButton.place(x=label.winfo_reqwidth() - 5 - subButton.winfo_reqwidth(), y=label.winfo_reqheight() - 5 - subButton.winfo_reqheight())
    windowObj.mainloop()

unborderedWindow()
