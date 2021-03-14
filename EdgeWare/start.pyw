import ctypes, hashlib, os, subprocess, time, webbrowser, zipfile, shutil, json, winsound, random as rand, threading as thread
from tkinter import messagebox

PATH = os.path.abspath(os.getcwd())
DESKTOP_PATH = os.path.join(os.environ['USERPROFILE'], 'Desktop')
AVOID_LIST = ['EdgeWare', 'AppData']
FILE_TYPES = ['png', 'jpg', 'jpeg']
RESOURCE_PATHS = ['\\resource\\', '\\resource\\aud', '\\resource\\img\\', '\\resource\\vid\\']
MAX_FILL_THREADS = 8
IMG_REPLACE_THRESH = 500

DEFAULT_WEB = '{"urls":["https://duckduckgo.com/"], "args":["?q=why+are+you+gay"]}'
DEFAULT_PROMPT = '{"moods":["no moods"], "freqList":[100], "minLen":0, "maxLen":1, "no moods":["no prompts"]}'
DEFAULT_DISCORD = 'Playing with myself~'

settingJsonObj = {}

def shortcutScript_gen(pth_str, keyword, script, title):
    #strings for batch script to write vbs script to create shortcut on desktop
    #stupid and confusing? yes. the only way i could find to do this? also yes.
    return ['@echo off\n'
            'set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"\n',
            'echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%\n',
            'echo sLinkFile = "%USERPROFILE%\Desktop\\' + title + '.lnk" >> %SCRIPT%\n',
            'echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%\n',
            'echo oLink.WorkingDirectory = "' + pth_str + '\\" >> %SCRIPT%\n',
            'echo oLink.IconLocation = "' + pth_str + '\\default_assets\\' + keyword + '_icon.ico" >> %SCRIPT%\n',
            'echo oLink.TargetPath = "' + pth_str + '\\' + script + '" >> %SCRIPT%\n',
            'echo oLink.Save >> %SCRIPT%\n',
            'cscript /nologo %SCRIPT%\n',
            'del %SCRIPT%']

#uses the above script to create a shortcut on desktop with given specs
def make_shortcut(tList):
    with open(PATH + '\\tmp.bat', 'w') as bat:
        bat.writelines(tList)
    try:
        subprocess.call(PATH + '\\tmp.bat')
        os.remove(PATH + '\\tmp.bat')
    except:
        print('failed')
    
liveFillThreads = 0 #count of live threads for hard drive filling
isPlayingAudio = False #audio thread flag
replaceThreadLive = False #replace thread flag

hasPromptJson = False #can use prompts flag

#for checking directories/files
def fileExists(dir):
    return os.path.exists(PATH + dir)

def desktopExists(obj):
    return os.path.exists(os.path.join(DESKTOP_PATH, obj))


def loadSettings():
    global settingJsonObj
    settingJsonObj = {}

    #creating objects to check vs used config for version updates
    with open(PATH + '\\configDefault.dat') as r:
        obj = r.readlines()
        varNames = obj[0].split(',')
        varNames[len(varNames)-1] = varNames[len(varNames)-1].replace('\n', '')
        defaultVars = obj[1].split(',')

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
        settingJsonObj['pip_installed'] = 1
        with open(PATH + '\\config.cfg', 'w') as f:
            f.write(json.dumps(settingJsonObj))

    #check pillow installed flag, if not installed attempt to install with pip
    if not int(settingJsonObj['pil_installed'])==1:
        try:
            subprocess.call('py -m pip install pillow')
        except:
            subprocess.call('pip install pillow')
        settingJsonObj['pil_installed'] = 1
        with open(PATH + '\\config.cfg', 'w') as f:
            f.write(json.dumps(settingJsonObj))
            
    #check pypresence installed flag, if not installed attempt to install with pip
    if not int(settingJsonObj['pypres_installed'])==1:
        try:
            subprocess.call('py -m pip install pypresence')
        except:
            subprocess.call('pip install pypresence')
        settingJsonObj['pypres_installed'] = 1
        with open(PATH + '\\config.cfg', 'w') as f:
            f.write(json.dumps(settingJsonObj))


#start init portion, check resources, config, etc.
try:
    if not fileExists('\\resource\\'):
        pth = 'pth-default_ignore'
        #selecting zip
        for obj in os.listdir(PATH + '\\'):
            try:
                if obj.split('.')[len(obj.split('.'))-1].lower() == 'zip':
                    pth = PATH + '\\' + obj
                    break
            except:
                print('{} is not a zip file.'.format(obj))
        #if found zip unpack
        if not pth == 'pth-default_ignore':
           with zipfile.ZipFile(pth, 'r') as obj:
                obj.extractall(PATH + '\\resource\\')
        else:
            #if no zip, use default resources
            for obj in RESOURCE_PATHS:
                os.mkdir(PATH + obj)
            dPath = PATH + '\\default_assets\\'
            oPath = PATH + '\\resource\\'
            shutil.copyfile(dPath + 'default_wallpaper.png', oPath + 'wallpaper.png')
            shutil.copyfile(dPath + 'default_image.png', oPath + 'img\\img0.png', follow_symlinks=True)
            if not os.path.exists(oPath + 'discord.dat'):
                with open(oPath + 'discord.dat', 'w') as f:
                    f.write(DEFAULT_DISCORD)
            if not os.path.exists(oPath + 'prompt.json'):
                with open(oPath + 'prompt.json', 'w') as f:
                    f.write(DEFAULT_PROMPT)
            if not os.path.exists(oPath + 'web.json'):
                with open(oPath + 'web.json', 'w') as f:
                    f.write(DEFAULT_WEB)
except:
    messagebox.showerror('Launch Error', 'Could not launch Edgeware.\nThere is no resource folder, and resource file could not be found.')
    os.kill(os.getpid(), 9)

if os.path.exists(PATH + '\\resource\\prompt.json'):
    hasPromptJson = True
if os.path.exists(PATH + '\\resource\\web.json'):
    hasWebJson = True

webJsonDat = ''
if os.path.exists(PATH + '\\resource\\web.json'):
    with open(PATH + '\\resource\\web.json', 'r') as webF:
        webJsonDat = json.loads(webF.read())

#load settings, if first run open options, then reload options from file
loadSettings()
if not settingJsonObj['is_configed']==1:
    subprocess.call('python config.pyw')
    loadSettings()


IMAGES = []
for img in os.listdir(PATH + '\\resource\\img\\'):
    IMAGES.append(PATH + '\\resource\\img\\' + img)
VIDEOS = []
for vid in os.listdir(PATH + '\\resource\\vid\\'):
    VIDEOS.append(PATH + '\\resource\\vid\\' + vid)
AUDIO = []
for aud in os.listdir(PATH + '\\resource\\aud\\'):
    AUDIO.append(PATH + '\\resource\\aud\\' + aud)

#set discord status if enabled
if int(settingJsonObj['showDiscord'])==1:
    try:
        os.startfile('disc_handler.pyw')
    except:
        print('silently failed to start discord status')

#making missing desktop shortcuts
if not desktopExists('Edgeware.lnk'):
    make_shortcut(shortcutScript_gen(PATH, 'default', 'start.pyw', 'Edgeware'))
if not desktopExists('Config.lnk'):
    make_shortcut(shortcutScript_gen(PATH, 'config', 'config.pyw', 'Config'))
if not desktopExists('Panic.lnk'):
    make_shortcut(shortcutScript_gen(PATH, 'panic', 'panicbutton.bat', 'Panic'))

#set wallpaper
if not int(settingJsonObj['hibernateMode'])==1:
    ctypes.windll.user32.SystemParametersInfoW(20, 0, PATH + '\\resource\\wallpaper.png', 0)

#selects url to be opened in new tab by web browser
def urlSelect(arg):
    return webJsonDat['urls'][arg] + webJsonDat['args'][arg].split(',')[rand.randrange(len(webJsonDat['args'][arg].split(',')))]

#main function, probably can do more with this but oh well i'm an idiot so
def main():
    if(not int(settingJsonObj['hibernateMode'])==1):
        annoyance()
    else:
        while True:
            waitTime = rand.randint(int(settingJsonObj['hibernateMin']), int(settingJsonObj['hibernateMax']))
            time.sleep(float(waitTime))
            ctypes.windll.user32.SystemParametersInfoW(20, 0, PATH + '\\resource\\wallpaper.png', 0)
            for i in range(0, rand.randint(int(int(settingJsonObj['wakeupActivity']) / 2), int(settingJsonObj['wakeupActivity']))):
                rollForInitiative()

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
        rollForInitiative()
        if(int(settingJsonObj['fill'])==1 and liveFillThreads < MAX_FILL_THREADS):
            thread.Thread(target=fillDrive).start()
        if(int(settingJsonObj['replace'])==1 and not replaceThreadLive):
            thread.Thread(target=replaceImages).start()
        time.sleep(float(settingJsonObj['delay']) / 1000.0)

#independtently attempt to do all active settings with probability equal to their freq value     
def rollForInitiative():
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
            tObj = str(time.time() * rand.randint(10000, 69420)).encode(encoding='ascii',errors='ignore')
            pth = os.path.join(root, hashlib.md5(tObj).hexdigest() + '.' + str.split(imageNames[index], '.')[len(str.split(imageNames[index], '.')) - 1].lower())
            shutil.copyfile(os.path.join(PATH, 'resource\\img', imageNames[index]), pth)
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

#let's goooooooooooooooooooooooooooooooooooooooo           
main()