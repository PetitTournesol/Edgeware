import tkinter as tk
from tkinter import *
import os

DEFAULT_CONFIG = '250;0;0;25;15;0;1'
PATH = os.path.abspath(os.getcwd())
if not os.path.exists(PATH + '/config.cfg'):
    with open(PATH + '/config.cfg', 'w') as f:
        f.write(DEFAULT_CONFIG)

root = tk.Tk()
root.title('EdgeWare Config')
root.resizable(False,False)
root.geometry('260x300')
root.iconbitmap(os.path.abspath(os.getcwd()) + '/resource/icon.ico')

def configWindow(delay, fill, replace, webMod, popupMod, server, slow):
    delayVar = IntVar(root, value=delay, name='delay')
    fillVar = IntVar(root, value=fill, name='fill')
    replaceVar = IntVar(root, value=replace, name='replace')
    webModVar = IntVar(root, value=webMod, name='webMod')
    popupModVar = IntVar(root, value=popupMod, name='popupMod')
    serverVar = IntVar(root, value=server, name='server')
    slowVar = IntVar(root, value=slow, name='slow')

    timerSlider = Scale(root, label='Timer Delay (ms)', from_=100, to=2000, orient=HORIZONTAL, variable=delayVar)
    timerSlider.set(delay)
    timerSlider.pack()
    webSlider = Scale(root, label='Website Freq', from_=0, to=100, orient=HORIZONTAL, variable=webModVar)
    webSlider.set(webMod)
    webSlider.pack()
    popupSlider = Scale(root, label='Popup Freq', from_=0, to=100, orient=HORIZONTAL, variable=popupModVar)
    popupSlider.set(popupMod)
    popupSlider.pack()
    isFill = Checkbutton(root, text='Fill Drive', variable=fillVar)
    isFill.pack()
    slowBox = Checkbutton(root, text='Slow Fill', variable=slowVar)
    slowBox.pack()
    isReplace = Checkbutton(root, text='Replace Images', variable=replaceVar)
    isReplace.pack()
    saveButton = Button(root, text='Save Config', command= lambda: save(delayVar.get(), fillVar.get(), replaceVar.get(), webModVar.get(), popupModVar.get(), serverVar.get(), slowVar.get()))
    saveButton.pack()
    root.mainloop()

def save(delay, fill, replace, webMod, popupMod, server, slow):
    with open('config.cfg', 'w') as f:
        f.write(str(delay) + ';' + str(int(fill)) + ';' + str(int(replace)) + ';' + str(webMod) + ';' + str(popupMod) + ';0;' + str(int(slow)))
    exit()

with open('config.cfg', 'r') as f:
    vals = f.readline().split(';')

configWindow(int(vals[0]), int(vals[1])==1, int(vals[2])==1, int(vals[3]), int(vals[4]), int(vals[5])==1, int(vals[6])==1)