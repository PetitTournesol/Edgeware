import os
import json
import random as rand
import tkinter as tk

from tkinter import messagebox
from tkinter import *

hasData = False
textData = {}
PATH = os.path.abspath(os.getcwd())
if(os.path.exists(PATH + '\\resource\\prompt.json')):
    hasData = True
    with open(PATH + '\\resource\\prompt.json', 'r') as f:
        textData = json.loads(f.read())

if(not hasData):
    messagebox.showerror('Prompt Error', 'Resource folder contains no "prompt.json". Either set prompt freq to 0 or add "prompt.json" to resource folder.')

def buildText():
    moodList = textData['moods']
    freqList = textData['freqList']
    outputPhraseCount = rand.randint(int(textData['minLen']), int(textData['maxLen']))
    strVar = ''
    selection = rand.choices(moodList, freqList, k=1)
    for i in range(outputPhraseCount):
        strVar += textData[selection[0]][rand.randrange(0, len(textData[selection[0]]))] + ' '
    return strVar.strip()

def unborderedWindow():
    if(not hasData):
        exit()
    windowObj = Tk()
    label = tk.Label(windowObj, text='\nType For Me~\n')
    label.pack()
    
    txt = buildText()

    wid = windowObj.winfo_screenwidth() / 4
    hgt = windowObj.winfo_screenheight() / 2

    textLabel = Label(windowObj, text=txt, wraplength=wid)
    textLabel.pack()

    windowObj.geometry('%dx%d+%d+%d' % (wid, hgt, 2*wid - wid / 2, hgt - hgt / 2))

    windowObj.overrideredirect(1)
    windowObj.frame = Frame(windowObj, borderwidth=2, relief=RAISED)
    windowObj.frame.pack_propagate(True)
    windowObj.wm_attributes('-topmost', 1)

    inputBox = Text(windowObj)
    inputBox.pack()

    subButton = Button(windowObj, text='I Submit <3', command= lambda: checkpass(txt, inputBox.get(1.0, "end-1c")))
    subButton.place(x=wid - 5 - subButton.winfo_reqwidth(), y=hgt - 5 - subButton.winfo_reqheight())
    windowObj.mainloop()

def checkpass(a, b):
    if(a == b):
        exit()

unborderedWindow()
