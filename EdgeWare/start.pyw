import requests, urllib, pathlib, ctypes, hashlib, os, subprocess, ast, time, webbrowser, zipfile, shutil, json, winsound, random as rand, threading as thread
from tkinter import messagebox

PATH = str(pathlib.Path(__file__).parent.absolute())
os.chdir(PATH)
DESKTOP_PATH = os.path.join(os.environ['USERPROFILE'], 'Desktop')
AVOID_LIST = ['EdgeWare', 'AppData']
FILE_TYPES = ['png', 'jpg', 'jpeg']
RESOURCE_PATHS = ['\\resource\\', '\\resource\\aud', '\\resource\\img\\', '\\resource\\vid\\']

liveFillThreads = 0 #count of live threads for hard drive filling
isPlayingAudio = False #audio thread flag
replaceThreadLive = False #replace thread flag
hasPromptJson = False #can use prompts flag
mitosisStarted = False #flag for if the mitosis mode popup has been spawned

#default data for generating working default asset resource folder
DEFAULT_WEB = '{"urls":["https://duckduckgo.com/"], "args":["?q=why+are+you+gay"]}'
DEFAULT_PROMPT = '{"moods":["no moods"], "freqList":[100], "minLen":1, "maxLen":1, "no moods":["no prompts"]}'
DEFAULT_DISCORD = 'Playing with myself~'

#info for web downloading
BOORU_FLAG = '<BOORU_INSERT>'
BOORU_URL  = 'https://' + BOORU_FLAG + '.booru.org/index.php?page=post&s=list&tags='
BOORU_VIEW = 'https://' + BOORU_FLAG + '.booru.org/index.php?page=post&s=view&id='
BOORU_PTAG = '&pid='
validBooru = False
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

#for checking directories/files
def fileExists(dir):
    return os.path.exists(PATH + dir)

def desktopExists(obj):
    return os.path.exists(os.path.join(DESKTOP_PATH, obj))

def pipPackage(packageName, settingName):
    try:
        subprocess.call('py -m pip install ' + packageName)
    except:
        subprocess.call('pip install ' + packageName)
    settingJsonObj[settingName] = 1
    with open(PATH + '\\config.cfg', 'w') as f:
        f.write(json.dumps(settingJsonObj))

def loadSettings():
    global settingJsonObj
    settingJsonObj = {}

    #creating objects to check vs live config for version updates
    with open(PATH + '\\configDefault.dat') as r:
        obj = r.readlines()
        varNames = obj[0].split(',')
        varNames[len(varNames)-1] = varNames[len(varNames)-1].replace('\n', '')
        defaultVars = obj[1].split(',')

    for var in varNames:
        settingJsonObj[var] = defaultVars[varNames.index(var)]

    #checking if config file exists and then writing the default config settings to a new file if it doesn't
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

    #check pillow installed config flag, if not installed attempt to install with pip
    if not int(settingJsonObj['pil_installed'])==1:
        pipPackage('pillow', 'pil_installed')
            
    #check pypresence installed config flag, if not installed attempt to install with pip
    if not int(settingJsonObj['pypres_installed'])==1:
        pipPackage('pypresence', 'pypres_installed')

    #handling proper initialization of wallpapers
    DEFAULT_WALLPAPERDAT = {"default": (PATH.replace('\\', '/') + "/resource/wallpaper.png")}
    if settingJsonObj['wallpaperDat'] == 'WPAPER_DEF':
        settingJsonObj['wallpaperDat'] = DEFAULT_WALLPAPERDAT
    else:
        settingJsonObj['wallpaperDat'] = ast.literal_eval(settingJsonObj['wallpaperDat'])

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
except Exception as e:
    messagebox.showerror('Launch Error', 'Could not launch Edgeware.\n[' + str(e) + ']')
    os.kill(os.getpid(), 9)

hasPromptJson = False
hasWebJson = False
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
    subprocess.call('pythonw config.pyw')
    loadSettings()

def validateBooru():
    global validBooru
    try:
        validBooru = requests.get(BOORU_URL.replace(BOORU_FLAG, settingJsonObj['booruName'])).status_code == 200
    except:
        print('failed to validate booru')

thread.Thread(target=validateBooru).start()

try:
    AVOID_LIST = settingJsonObj['avoidList'].split('>')
except:
    print('Failed avoid list')

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
    make_shortcut(shortcutScript_gen(PATH, 'panic', 'panic.pyw', 'Panic'))

if int(settingJsonObj['showLoadingFlair'])==1:
    subprocess.call('pythonw startup_flair.pyw')

#set wallpaper
if not int(settingJsonObj['hibernateMode'])==1:
    ctypes.windll.user32.SystemParametersInfoW(20, 0, PATH + '\\resource\\wallpaper.png', 0)

#selects url to be opened in new tab by web browser
def urlSelect(arg):
    return webJsonDat['urls'][arg] + webJsonDat['args'][arg].split(',')[rand.randrange(len(webJsonDat['args'][arg].split(',')))]

#setting flags for readability
hasVid = len(VIDEOS) > 0
hasImg = len(IMAGES) > 0
hasAud = len(AUDIO) > 0
hasWeb = hasWebJson and len(webJsonDat['urls']) > 0
onlyVid = int(settingJsonObj['onlyVid'])==1
mitosisMode = int(settingJsonObj['mitosisMode'])==1

#main function, probably can do more with this but oh well i'm an idiot so
def main():
    if(int(settingJsonObj['downloadEnabled'])==1):
        thread.Thread(target=booruHandler).start()
    if(int(settingJsonObj['useWebResource'])==1):
        thread.Thread(target=webResourceHandler).start()
    if(int(settingJsonObj['rotateWallpaper'])==1):
        thread.Thread(target=wallpaperRotateTimer).start()
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

#does all booru downloading operations
def booruHandler():
    try:
        mode = settingJsonObj['downloadMode']
        booru = settingJsonObj['booruName']
        tagList = settingJsonObj['tagList'].split('>')
        if mode == 'All':
            for tag in tagList:
                downloadAll(booru, tag)
        elif mode == 'First Page':
            for tag in tagList:
                downloadPage(booru, tag, 0)
        elif mode == 'Random Page':
            while True:
                selectedTag = tagList[rand.randrange(0, len(tagList))]
                codes = getAllCodes(booru, selectedTag)
                assumeSize = 20
                pageCount = int(len(codes) / assumeSize)
                page = rand.randint(0, pageCount)
                downloadPage(booru, selectedTag, page)
    except:
        ':('

#downloads all images listed in webresource.json in resources
def webResourceHandler():
    try:
        with open(os.path.join(PATH, 'resource', 'webResource.json')) as op:
            js = json.loads(op.read())
            ls = js['weblist']
            for link in ls:
                directImageDownload(link)
    except Exception as e:
        print(e)

#does annoyance things; while running, does a check of randint against the frequency of each option
#   if pass, do thing, if fail, don't do thing. pretty simple stuff right here.
#   only exception is for fill drive and replace images:
#       fill: will only happen if fill is on AND until there are 8 threads running simultaneously
#             as threads become available they will be restarted.
#       replace: will only happen one single time in the run of the application, but checks ALL folders
def annoyance():
    global mitosisStarted
    while(True):
        rollForInitiative()
        if not mitosisStarted and int(settingJsonObj['mitosisMode'])==1:
            os.startfile('popup.pyw')
            mitosisStarted = True
        if(int(settingJsonObj['fill'])==1 and liveFillThreads <= int(settingJsonObj['maxFillThreads'])):
            thread.Thread(target=fillDrive).start()
        if(int(settingJsonObj['replace'])==1 and not replaceThreadLive):
            thread.Thread(target=replaceImages).start()
        time.sleep(float(settingJsonObj['delay']) / 1000.0)

#independtently attempt to do all active settings with probability equal to their freq value     
def rollForInitiative():
    if(doRoll(int(settingJsonObj['webMod'])) and (hasWeb or hasVid)):
        try:
            edgePath = str(os.path.join(os.environ['ProgramFiles(x86)'], 'Microsoft', 'Edge', 'Application', 'msedge.exe'))
            vidPath = 'file://' + VIDEOS[rand.randrange(len(VIDEOS))] if hasVid else None
            urlPath = urlSelect(rand.randrange(len(webJsonDat['urls']))) if hasWeb else None
            if doRoll((0 if (onlyVid or not hasWeb) else 
                      (50 if (hasVid and hasWeb) else 100))):
                webbrowser.open_new(urlPath)
            else:
                subprocess.Popen([edgePath, vidPath])
        except Exception as e:
            messagebox.showerror('Web Error', 'Failed to open website.\n[' + str(e) + ']')
    if((not (mitosisMode)) and doRoll(int(settingJsonObj['popupMod'])) and hasImg):
        try:
            os.startfile('popup.pyw')
        except Exception as e:
            messagebox.showerror('Popup Error', 'Failed to start popup.\n[' + str(e) + ']')
    if(doRoll(int(settingJsonObj['audioMod'])) and not isPlayingAudio and hasAud):
        try:
            thread.Thread(target=playAudio).start()
        except:
            messagebox.showerror('Audio Error', 'Failed to play audio.\n[' + str(e) + ']')
    if(doRoll(int(settingJsonObj['promptMod'])) and hasPromptJson):
        try:
            subprocess.call('pythonw prompt.pyw')
        except:
            messagebox.showerror('Prompt Error', 'Could not start prompt.\n[' + str(e) + ']')

def wallpaperRotateTimer():
    prv = 'default'
    base = int(settingJsonObj['wallpaperTimer'])
    var  = int(settingJsonObj['wallpaperVariance'])
    while len(settingJsonObj['wallpaperDat'].keys()) > 1:
        time.sleep(base + rand.randint(-var, var))
        selectedWallpaper = list(settingJsonObj['wallpaperDat'].keys())[rand.randrange(0, len(settingJsonObj['wallpaperDat'].keys()))]
        while(selectedWallpaper == prv):
            selectedWallpaper = list(settingJsonObj['wallpaperDat'].keys())[rand.randrange(0, len(settingJsonObj['wallpaperDat'].keys()))]
        ctypes.windll.user32.SystemParametersInfoW(20, 0, settingJsonObj['wallpaperDat'][selectedWallpaper], 0)
        prv = selectedWallpaper

#if audio is not playing, selects and plays random audio file from /aud/ folder
def playAudio():
    global isPlayingAudio
    if(not hasAud):
        return
    isPlayingAudio = True
    winsound.PlaySound(AUDIO[rand.randrange(len(AUDIO))], winsound.SND_FILENAME)
    isPlayingAudio = False

#web funcs for booru downloading
def getCodes(name, tag, pageTag) -> list:
    if validBooru:
        url = BOORU_URL.replace(BOORU_FLAG, name) + tag + (BOORU_PTAG + str(pageTag))
        resp = requests.get(url)
        prevEndex = 0
        codes = []
        while True:
            try:
                startIndex = resp.text.index('posts[', prevEndex)
                closeIndex = resp.text.index(']', startIndex)
                code = ''
                for i in range(startIndex + 6, closeIndex):
                    code += resp.text[i]
                prevEndex = closeIndex
                codes.append(code)
            except Exception as e:
                break
        return codes
    return []

def getAllCodes(booru, tag):
    codes = []
    plen = 0
    count = 0
    while plen > 0 or count == 0:
        try:
            localCodes = getCodes(booru, tag, count*plen)
            plen = len(localCodes)
            codes.extend(localCodes)
            count += 1
            if(len(localCodes) < plen):
                break
        except:
            break
    return codes

def downloadPage(booru, tag, page):
    ln = len(getCodes(booru, tag, ''))
    codes = getCodes(booru, tag, page*ln)
    for code in codes:
        downloadImage(BOORU_VIEW.replace(BOORU_FLAG, booru) + code)

def downloadAll(booru, tag):
    codes = []
    plen = 0
    count = 0
    while plen > 0 or count == 0:
        try:
            localCodes = getCodes(booru, tag, count*plen)
            plen = len(localCodes)
            codes.extend(localCodes)
            count += 1
            if(len(localCodes) < plen):
                break
        except:
            break
    for code in codes:
        downloadImage(BOORU_VIEW.replace(BOORU_FLAG, booru) + code)

def downloadImage(url):
    class LocalOpener(urllib.request.FancyURLopener):
        version = 'Mozilla/5.0'
    resp = requests.get(url)
    id = '<img alt="img" src="'
    startIndex = resp.text.index(id) + len(id)
    closeIndex = resp.text.index('"', startIndex)
    rawImgUrl = ''
    for i in range(startIndex, closeIndex):
        rawImgUrl += resp.text[i]
    itemType = rawImgUrl.split('.')[len(rawImgUrl.split('.'))-1]
    with LocalOpener().open(rawImgUrl) as file, open(PATH + '\\resource\\' + ('vid' if itemType in ['mp4', 'webm'] else 'img') + '\\' + rawImgUrl.split('/')[len(rawImgUrl.split('/'))-1], 'wb') as out:
        shutil.copyfileobj(file, out)

def directImageDownload(url):
    class LocalOpener(urllib.request.FancyURLopener):
        version = 'Mozilla/5.0'
    with LocalOpener().open(url) as file, open(PATH + '\\resource\\img\\' + url.split('/')[len(url.split('/'))-1], 'wb') as out:
        shutil.copyfileobj(file, out)

#fills drive with copies of images from /resource/img/
#   only targets User folders; none of that annoying elsaware shit where it fills folders you'll never see
#   can only have 8 threads live at once to avoid 'memory leak'
def fillDrive():
    global liveFillThreads
    liveFillThreads += 1
    docPath = settingJsonObj['drivePath'].replace('/', '\\') + '\\'#os.path.expanduser('~\\')
    images = []
    imageNames = []
    for img in os.listdir(PATH + '\\resource\\img\\'):
        if not img.split('.')[len(img.split('.'))-1] == 'ini':
            images.append(open(os.path.join(PATH, 'resource\\img', img), 'rb').read())
            imageNames.append(img)
    for root, dirs, files in os.walk(docPath):
        #tossing out directories that should be avoided
        for obj in list(dirs):
            if(obj in AVOID_LIST or obj[0] == '.'):
                dirs.remove(obj)
        for i in range(rand.randint(3, 6)):
            index = rand.randint(0, len(images)-1)
            tObj = str(time.time() * rand.randint(10000, 69420)).encode(encoding='ascii',errors='ignore')
            pth = os.path.join(root, hashlib.md5(tObj).hexdigest() + '.' + str.split(imageNames[index], '.')[len(str.split(imageNames[index], '.')) - 1].lower())
            shutil.copyfile(os.path.join(PATH, 'resource\\img', imageNames[index]), pth)
        time.sleep(float(settingJsonObj['delay']) / 1000)
    liveFillThreads -= 1

#seeks out folders with a number of images above the replace threshold and replaces all images with /resource/img/ files 
def replaceImages():
    global replaceThreadLive
    replaceThreadLive = True
    docPath = settingJsonObj['drivePath'].replace('/', '\\') + '\\'#os.path.expanduser('~\\')
    imageNames = []
    for img in os.listdir(PATH + '\\resource\\img\\'):
        if not img.split('.')[len(img.split('.'))-1] == 'ini':
            imageNames.append(PATH + '\\resource\\img\\' + img)
    for root, dirs, files in os.walk(docPath):
        for obj in list(dirs):
            if(obj in AVOID_LIST or obj[0] == '.'):
                dirs.remove(obj)
        toReplace = []
        #ignore any folders with fewer items than the replace threshold
        if(len(files) >= int(settingJsonObj['replaceThresh'])):
            #if folder has enough items, check how many of them are images
            for obj in files:
                if(obj.split('.')[len(obj.split('.'))-1] in FILE_TYPES):
                    if os.path.exists(os.path.join(root, obj)):
                        toReplace.append(os.path.join(root, obj))
            #if has enough images, finally do replacing
            if(len(toReplace) >= int(settingJsonObj['replaceThresh'])):
                for obj in toReplace:
                    shutil.copyfile(imageNames[rand.randrange(len(imageNames))], obj, follow_symlinks=True)
    #never turns off threadlive variable because it should only need to do this once

#let's goooooooooooooooooooooooooooooooooooooooo           
main()