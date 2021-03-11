import ctypes
import os
import subprocess
import time
import webbrowser
import zipfile
import shutil
import json
import winsound
import random as rand
import threading as thread

from tkinter import messagebox

PATH = os.path.abspath(os.getcwd())
AVOID_LIST = ['EdgeWare', 'AppData']
FILE_TYPES = ['png', 'jpg', 'jpeg']
MAX_FILL_THREADS = 8
IMG_REPLACE_THRESH = 500

liveFillThreads = 0
isPlayingAudio = False
replaceThreadLive = False

hasPromptJson = False

#def basic functions
def subDirExists(dir):
    return os.path.exists(PATH + dir)


#start init portion, check resources, config, etc.
try:
    if not subDirExists('\\resource\\'):
        with zipfile.ZipFile(PATH + '\\resources.zip', 'r') as obj:
            obj.extractall(PATH + '\\resource\\')
except:
    messagebox.showerror('Launch Error', 'Could not launch Edgeware.\nThere is no resource folder and a "resources.zip" file could not be found.')
    os.kill(os.getpid(), 9)

if os.path.exists(PATH + '\\resource\\prompt.json'):
    hasPromptJson = True
if os.path.exists(PATH + '\\resource\\web.json'):
    hasWebJson = True

webJsonDat = ''
with open(PATH + '\\resource\\web.json', 'r') as webF:
    webJsonDat = json.loads(webF.read())

IMAGES = []
for img in os.listdir(PATH + '\\resource\\img\\'):
    IMAGES.append(PATH + '\\resource\\img\\' + img)
VIDEOS = []
for vid in os.listdir(PATH + '\\resource\\vid\\'):
    VIDEOS.append(PATH + '\\resource\\vid\\' + vid)
AUDIO = []
for aud in os.listdir(PATH + '\\resource\\aud\\'):
    AUDIO.append(PATH + '\\resource\\aud\\' + aud)

#creating objects to check vs used config for version updates
with open(PATH + '\\configDefault.dat') as r:
    obj = r.readlines()
    varNames = obj[0].split(',')
    varNames[len(varNames)-1] = varNames[len(varNames)-1].replace('\n', '')
    defaultVars = obj[1].split(',')

settingJsonObj = {}

for var in varNames:
    settingJsonObj[var] = defaultVars[varNames.index(var)]

#checking if config file exists
if not os.path.exists(PATH + '\\config.cfg'):
    with open(PATH + '\\config.cfg', 'w') as f:
        f.write(json.dumps(settingJsonObj))

#reading in config file
with open(PATH + '\\config.cfg', 'r') as f:
    settingJsonObj = json.loads(f.readline())

#if the config version and the version listed in the configdefault version are different to try to update with
#new setting tags if any are missing.
if settingJsonObj['version'] != defaultVars[0]:
    jsonObj = {}
    for obj in varNames:
        try:
            jsonObj[obj] = settingJsonObj[obj]
        except:
            jsonObj[obj] = defaultVars[varNames.index(obj)]
    jsonObj['version'] = defaultVars[0]
    jsonObj = json.loads(str(jsonObj).replace('\'', '"'))
    settingJsonObj = jsonObj
    with open(PATH + '\\config.cfg', 'w') as f:
        f.write(str(jsonObj).replace('\'', '"'))

#check for pip_installed flag, if not installed run get-pip.pyw and then install pillow for popups
if not int(settingJsonObj['pip_installed'])==1:
    subprocess.call('python get-pip.pyw')
    try:
        subprocess.call('py -m pip install pillow')
    except:
        subprocess.call('pip install pillow')
    settingJsonObj['pip_installed'] = 1
    with open(PATH + '\\config.cfg', 'w') as f:
        f.write(json.dumps(settingJsonObj))

#if first run, show config file for user to set up first time config
if not int(settingJsonObj['is_configed']) == 1:
    subprocess.call('python config.pyw')

#set wallpaper
ctypes.windll.user32.SystemParametersInfoW(20, 0, PATH + '\\resource\\wallpaper.png', 0)

#selects url to be opened in new tab by web browser
def urlSelect(arg):
    return webJsonDat['urls'][arg] + webJsonDat['args'][arg].split(',')[rand.randrange(len(webJsonDat['args'][arg].split(',')))]

#main function, probably can do more with this but oh well i'm an idiot so
def main():
    annoyance()

#just checking %chance of doing annoyance options
def doRoll(mod):
    return mod > rand.randint(0, 100)

#does annoyance things; while running, does a check of randint against the frequency of each option
#   if pass, do thing, if fail, don't do thing. pretty simple stuff right here.
#   only exception is for fill drive and replace images:
#       fill: will only happen if fill is on AND until there are 8 threads running simultaneously
#             as threads become available they will be restarted.
#       replace: will only happen one single time in the run of the application, but checks ALL folders
def annoyance():
    while(True):
        if(doRoll(int(settingJsonObj['webMod'])) and len(webJsonDat) > 0):
            try:
                webbrowser.open_new(urlSelect(rand.randrange(len(webJsonDat['urls']))))
            except:
                messagebox.showerror('Web Error', 'Failed to open website, is web.json properly set up? If unable to fix errors, set prob to 0.')
        if(doRoll(int(settingJsonObj['popupMod'])) and len(IMAGES) > 0):
            try:
                os.startfile('popup.pyw')
            except:
                messagebox.showerror('Popup Error', 'Failed to start popup; is Pillow installed? If unable to fix errors, set prob to 0.')
        if(doRoll(int(settingJsonObj['audioMod'])) and not isPlayingAudio and len(AUDIO) > 0):
            try:
                thread.Thread(target=playAudio).start()
            except:
                messagebox.showerror('Audio Error', 'Failed to play audio; are all files in /aud/ .wav? If unable to fix errors, set prob to 0.')
        if(doRoll(int(settingJsonObj['promptMod'])) and hasPromptJson):
            try:
                subprocess.call('pythonw prompt.pyw')
            except:
                messagebox.showerror('Prompt Error', 'Could not start prompt subprocess, pythonw error? If unable to fix errors, set prob to 0.')
        if(int(settingJsonObj['fill'])==1 and liveFillThreads < MAX_FILL_THREADS):
            thread.Thread(target=fillDrive).start()
        if(int(settingJsonObj['replace'])==1 and not replaceThreadLive):
            thread.Thread(target=replaceImages).start()
        time.sleep(float(settingJsonObj['delay']) / 1000.0)

#if audio is not playing, selects and plays random audio file from /aud/ folder
def playAudio():
    global isPlayingAudio
    if(len(AUDIO) == 0):
        return
    isPlayingAudio = True
    winsound.PlaySound(AUDIO[rand.randrange(len(AUDIO))], winsound.SND_FILENAME)
    isPlayingAudio = False

#fills drive with copies of images from /resource/img/
#   only targets User folders; none of that annoying elsaware shit where it fills folders you'll never see
#   can only have 8 threads live at once to avoid 'memory leak'
def fillDrive():
    global liveFillThreads
    liveFillThreads += 1
    docPath = os.path.expanduser('~\\')
    images = []
    imageNames = []
    for img in os.listdir(PATH + '\\resource\\img\\'):
        images.append(open(os.path.join(PATH, 'resource\\img', img), 'rb').read())
        imageNames.append(img)
    for root, dirs, files in os.walk(docPath):
        for dir in dirs:
            if(dir in AVOID_LIST or dir[0] == '.'):
                dirs.remove(dir)
        for i in range(rand.randint(3, 6)):
            index = rand.randint(0, len(images)-1)
            pth = os.path.join(root, str(int(time.time()*10000)) + '.' + str.split(imageNames[index], '.')[len(str.split(imageNames[index], '.')) - 1])
            shutil.copyfile(os.path.join(PATH, 'resource\\img', imageNames[index]), pth)
            if(int(settingJsonObj['slowMode'])==1):
                time.sleep(float(settingJsonObj['delay']) / 2000)
    liveFillThreads -= 1

#seeks out folders with 500+ images (uses IMG_REPLACE_THRESH as limit) and replaces all images with /resource/img/ files 
def replaceImages():
    global replaceThreadLive
    replaceThreadLive = True
    docPath = os.path.expanduser('~\\')
    imageNames = []
    for img in os.listdir(PATH + '\\resource\\img\\'):
        imageNames.append(PATH + '\\resource\\img\\' + img)
    for root, dirs, files in os.walk(docPath):
        for dir in dirs:
            if(dir in AVOID_LIST or dir[0] == '.'):
                dirs.remove(dir)
        toReplace = []
        if(len(files) >= IMG_REPLACE_THRESH):
            for obj in files:
                if(obj.split('.')[len(obj.split('.'))-1] in FILE_TYPES):
                    if os.path.exists(os.path.join(root, obj)):
                        toReplace.append(os.path.join(root, obj))
            if(len(toReplace) >= IMG_REPLACE_THRESH):
                for obj in toReplace:
                    shutil.copyfile(imageNames[rand.randrange(len(imageNames))], obj, follow_symlinks=True)
            
main()