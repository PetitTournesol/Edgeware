import os, pathlib, json, random as rand, tkinter as tk
from tkinter import messagebox
from tkinter import *

hasData = False
textData = {}
maxMistakes = 3
PATH = str(pathlib.Path(__file__).parent.absolute())
os.chdir(PATH)

with open(PATH + '\\config.cfg') as settings:
    maxMistakes = int(json.loads(settings.read())['promptMistakes'])

if(os.path.exists(PATH + '\\resource\\prompt.json')):
    hasData = True
    with open(PATH + '\\resource\\prompt.json', 'r') as f:
        textData = json.loads(f.read())

if(not hasData):
    messagebox.showerror('Prompt Error', 'Resource folder contains no "prompt.json". Either set prompt freq to 0 or add "prompt.json" to resource folder.')

def unborderedWindow():
    if(not hasData):
        exit()
    root = Tk()
    label = tk.Label(root, text='\nType For Me, Slut~\n')
    label.pack()
    
    txt = buildText()

    wid = root.winfo_screenwidth() / 4
    hgt = root.winfo_screenheight() / 2

    textLabel = Label(root, text=txt, wraplength=wid)
    textLabel.pack()

    root.geometry('%dx%d+%d+%d' % (wid, hgt, 2*wid - wid / 2, hgt - hgt / 2))

    root.overrideredirect(1)
    root.frame = Frame(root, borderwidth=2, relief=RAISED)
    root.frame.pack_propagate(True)
    root.wm_attributes('-topmost', 1)

    inputBox = Text(root)
    inputBox.pack()

    subButton = Button(root, text='I Submit <3', command=lambda: checkTotal(root, txt, inputBox.get(1.0, "end-1c")))
    subButton.place(x=wid - 5 - subButton.winfo_reqwidth(), y=hgt - 5 - subButton.winfo_reqheight())
    root.mainloop()

def buildText():
    moodList = textData['moods']
    freqList = textData['freqList']
    outputPhraseCount = rand.randint(int(textData['minLen']), int(textData['maxLen']))
    strVar = ''
    selection = rand.choices(moodList, freqList, k=1)
    for i in range(outputPhraseCount):
        strVar += textData[selection[0]][rand.randrange(0, len(textData[selection[0]]))] + ' '
    return strVar.strip()

def checkTotal(root, a, b):
    if checkText(a, b):
        root.destroy()

def checkText(a, b):
    mistakes = 0
    if len(a) != len(b):
        mistakes += abs(len(a)-len(b))
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            mistakes += 1
    return mistakes <= maxMistakes

try:
    unborderedWindow()
except Exception as e:
    messagebox.showerror('Prompt Error', 'Could not create prompt window.\n[' + str(e) + ']')