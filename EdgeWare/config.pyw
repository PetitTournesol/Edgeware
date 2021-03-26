import json, os, urllib.request, shutil, webbrowser, zipfile, pathlib
from tkinter import Tk, ttk, simpledialog, messagebox, filedialog
from tkinter import *

PATH = str(pathlib.Path(__file__).parent.absolute()) + '\\'

#text for the about tab
ANNOYANCE_TEXT = 'The "Annoyance" section consists of the 5 main configurable settings of Edgeware:\nDelay\nPopup Frequency\nWebsite Frequency\nAudio Frequency\nPromptFrequency\n\nEach is fairly self explanatory, but will still be expounded upon in this section. Delay is the forced time delay between each tick of the "clock" for Edgeware. The longer it is, the slower things will happen. Popup frequency is the percent chance that a randomly selected popup will appear on any given tick of the clock, and similarly for the rest, website being the probability of opening a website, audio for playing a file from /resource/aud/, and prompt for a typing prompt to pop up.\n\nThese values can be set by adjusting the bars, or by clicking the button beneath each respective slider, which will allow you to type in an explicit number instead of searching for it on the scrollbar.\n\nIn order to disable any feature, lower its probability to 0, to ensure that you\'ll be getting as much of any feature as possible, turn it up to 100.'
DRIVE_TEXT = 'The "Drive" portion of Edgeware has two features, fill drive and replace images.\n\n"Fill Drive" does exactly what it says: it attempts to fill your hard drive with as much porn from /resource/img/ as possible. It does, however, have some restrictions. It will (should) not place ANY images into folders that start with a ".", are named "EdgeWare", or that are named "Appdata".\nIt will also ONLY place images into your User folder and its subfolders; no more picking images out of system files for hours, just disentangling all of your stuff from them.\nFill drive has one modifier, which is its own forced delay. Because it runs with between 1 and 8 threads at any given time, when unchecked it can fill your drive VERY quickly. To ensure that you get that nice slow fill, you can adjust the delay between each folder sweep it performs.\n\n"Replace Images" is more complicated. Its searching is the exact same as fill drive, but instead of throwing images everywhere, it will seek out folders with large numbers of images (more than the threshold value) and when it finds one, it will replace ALL of the images with porn from /resource/img/. REMEMBER THAT IF YOU CARE ABOUT YOUR PHOTOS, AND THEY\'RE IN A FOLDER WITH MORE IMAGES THAN YOUR CHOSEN THRESHOLD VALUE, EITHER BACK THEM UP IN A ZIP OR SOMETHING OR DO. NOT. USE. THIS SETTING. I AM NOT RESPONSIBLE FOR YOUR OWN DECISION TO RUIN YOUR PHOTOS.'
STARTUP_TEXT = 'Start on launch does exactly what it says it does and nothing more: it allows Edgeware to start itself whenever you start up and log into your PC.\n\nPlease note that the method used does NOT edit registry or schedule any tasks. The "lazy startup" method was used for both convenience of implementation and convenience of cleaning.\n\nIf you forget to turn off the "start on logon" setting before uninstalling, you will need to manually go to your Startup folder and remove "edgeware.bat".'
HIBERNATE_TEXT = 'The Hibernate feature is an entirely different mode for Edgeware to operate in.\nInstead of constantly shoving popups, lewd websites, audio, and prompts in your face, hibernate starts quiet and waits for a random amount of time between its provided min and max before exploding with a rapid assortment of your chosen payloads. Once it finishes its barrage, it settles back down again for another random amount of time, ready to strike again when the time is right.\n\n\nThis feature is intend to be a much "calmer" way to use Edgeware; instead of explicitly using it to edge yourself or get off, it\'s supposed to lie in wait for you and perform bursts of self-sabotage to keep drawing you back to porn.'
ADVANCED_TEXT = 'The Advanced section is also something previously only accessible by directly editing the config.cfg file. It offers full and complete customization of all setting values without any limitations outside of variable typing.\n\n\nPlease use this feature with discretion, as any erroneous values will result in a complete deletion and regeneration of the config file from the default, and certain value ranges are likely to result in crashes or unexpected glitches in the program.'
THANK_AND_ABOUT_TEXT = 'Thank you so much to all the fantastic artists who create and freely distribute the art that allows programs like this to exist, to all the people who helped me work through the various installation problems as we set the software up (especially early on), and honestly thank you to ALL of the people who are happily using Edgeware. \n\nIt truly makes me happy to know that my work is actually being put to good use by people who enjoy it. After all, at the end of the day that\'s really all I\'ve ever really wanted, but figured was beyond reach of a stupid degreeless neet.\nI love you all <3\n\n\n\nIf you like my work, please feel free to help support my neet lifestyle by donating to $PetitTournesol on Cashapp; by no means are you obligated or expected to, but any and all donations are greatly appreciated!'

#google is a bitch so this is temporarily shelved
#DOWNLOAD_STRINGS = ['Blacked', 'Yiff', 'Censor', 'Hypno', 'Goon']
#DOWNLOAD_LINKS   = ['1BHLrCO5cvm9YCF_EeWGYS8AmAsPxUZPJ',
#                    '1b2gOJBLy-nD5p1cOM8xTDPh7LGsf1g5',
#                    '',
#                    '',
#                    '5pzl&id=1GhJQ7OtL9hblQJ4NTLP3Nz23AKcUqdz-']
#URL_BASE = 'https://docs.google.com/uc?export=download&confirm='

UPDCHECK_URL = 'https://raw.githubusercontent.com/PetitTournesol/Edgeware/main/EdgeWare/configDefault.dat'
local_version = '[?]'
with open(PATH + 'configDefault.dat') as r:
    obj = r.readlines()
    varNames = obj[0].split(',')
    varNames[len(varNames)-1] = varNames[len(varNames)-1].replace('\n', '')
    defaultVars = obj[1].split(',')

local_version = defaultVars[0]

settingJsonObj = {}
for var in varNames:
    settingJsonObj[var] = defaultVars[varNames.index(var)]

defaultJsonObj = settingJsonObj.copy()

if not os.path.exists(PATH + 'config.cfg'):
    with open(PATH + 'config.cfg', 'w') as f:
        f.write(json.dumps(settingJsonObj))

with open(PATH + 'config.cfg', 'r') as f:
    settingJsonObj = json.loads(f.readline())

if settingJsonObj['version'] != defaultVars[0]:
    jsonObj = {}
    for obj in varNames:
        try:
            jsonObj[obj] = settingJsonObj[obj]
        except:
            jsonObj[obj] = defaultVars[varNames.index(obj)]
    jsonObj['version'] = defaultVars[0]
    settingJsonObj = jsonObj
    with open(PATH + 'config.cfg', 'w') as f:
        f.write(str(jsonObj).replace('\'', '"'))

def spawnWindow():
    global settingJsonObj, defaultJsonObj
    webv = getLiveVersion()

    #window things
    root = Tk()
    root.title('Edgeware Config')
    #root.resizable(False, False)
    root.geometry('625x530')
    root.iconbitmap(PATH + 'default_assets\\config_icon.ico')
    #root.wm_attributes('-topmost', 1)
    fail_loop = 0

    #painful control variables ._.
    while(True and fail_loop < 2):
        try:
            delayVar = IntVar(root, value=int(settingJsonObj['delay']))
            popupVar = IntVar(root, value=int(settingJsonObj['popupMod']))
            webVar = IntVar(root, value=int(settingJsonObj['webMod']))
            audioVar = IntVar(root, value=int(settingJsonObj['audioMod']))
            promptVar = IntVar(root, value=int(settingJsonObj['promptMod']))
            fillVar = BooleanVar(root, value=(settingJsonObj['fill']==1))
            fillDelayVar = IntVar(root, value=int(settingJsonObj['fill_delay']))
            replaceVar = BooleanVar(root, value=(settingJsonObj['replace'] == 1))
            replaceThreshVar = IntVar(root, value=int(settingJsonObj['replaceThresh']))
            startLoginVar = BooleanVar(root, value=(settingJsonObj['start_on_logon'] == 1))
            hibernateVar = BooleanVar(root, value=(settingJsonObj['hibernateMode']==1))
            hibernateMinVar = IntVar(root, value=int(settingJsonObj['hibernateMin']))
            hibernateMaxVar = IntVar(root, value=(settingJsonObj['hibernateMax']))
            wakeupActivityVar = IntVar(root, value=(settingJsonObj['wakeupActivity']))
            discordVar = BooleanVar(root, value=(int(settingJsonObj['showDiscord'])==1))
            startFlairVar = BooleanVar(root, value=(int(settingJsonObj['showLoadingFlair'])==1))
            captionVar = BooleanVar(root, value=(int(settingJsonObj['showCaptions'])==1))
            panicButtonVar = IntVar(root, value=settingJsonObj['panicButton'])
            panicVar = BooleanVar(root, value=(int(settingJsonObj['panicDisabled'])==1))
            promptMistakeVar = IntVar(root, value=int(settingJsonObj['promptMistakes']))
            #zipDropVar = StringVar(root, value=DOWNLOAD_STRINGS[0])
            #grouping for sanity's sake later
            in_var_group = [delayVar, popupVar, webVar, audioVar, promptVar, fillVar, fillDelayVar, replaceVar, replaceThreshVar, startLoginVar, hibernateVar, hibernateMinVar, hibernateMaxVar, wakeupActivityVar, discordVar, startFlairVar, captionVar, panicButtonVar, panicVar, promptMistakeVar]
            in_var_names = ['delay', 'popupMod', 'webMod', 'audioMod', 'promptMod', 'fill', 'fill_delay', 'replace', 'replaceThresh', 'start_on_logon', 'hibernateMode', 'hibernateMin', 'hibernateMax', 'wakeupActivity', 'showDiscord', 'showLoadingFlair', 'showCaptions', 'panicButton', 'panicDisabled', 'promptMistakes']
            break
        except Exception as e:
            messagebox.showwarning('Settings Warning', 'File "config.cfg" appears corrupted.\nFile will be restored to default.\n[' + str(e) + ']')
            jObj = {}
            for var in varNames:
                jObj[var] = defaultVars[varNames.index(var)]
            with open(PATH + 'config.cfg', 'w') as f:
                f.write(json.dumps(jObj))
            with open(PATH + 'config.cfg', 'r') as f:
                settingJsonObj = json.loads(f.readline())
            fail_loop += 1
            
    #done painful control variables

    #for grouping
    hibernate_group = []
    fill_group = []
    replace_group = []

    #tab display code start
    tabMaster = ttk.Notebook(root)          #tab manager
    tabGeneral = ttk.Frame(None)            #general tab, will have current settings
    tabJSON = ttk.Frame(None)               #tab for JSON editor (unused)
    tabAdvanced = ttk.Frame(None)           #advanced tab, will have settings pertaining to startup, hibernation mode settings
    tabInfo = ttk.Frame(None)               #info, github, version, about, etc.

    style = ttk.Style(root)                 #style setting for left aligned tabs
    style.configure('lefttab.TNotebook', tabposition='wn')
    tabInfoExpound = ttk.Notebook(tabInfo, style='lefttab.TNotebook')  #additional subtabs for info on features

    tab_annoyance = ttk.Frame(None)
    tab_drive = ttk.Frame(None)
    tab_launch = ttk.Frame(None)
    tab_hibernate = ttk.Frame(None)
    tab_advanced = ttk.Frame(None)
    tab_thanksAndAbout = ttk.Frame(None)

    tabMaster.add(tabGeneral, text='General')
    #==========={IN HERE IS GENERAL TAB ITEM INITS}===========#
    #init
        #delay row
    delayScale = Scale(tabGeneral, label='Timer Delay (ms)', from_=10, to=60000, orient='horizontal', variable=delayVar)
    delayManual = Button(tabGeneral, text='Manual delay...', command=lambda: assign(delayVar, simpledialog.askinteger('Manual Delay', prompt='[10-60000]: ')))
    popupScale = Scale(tabGeneral, label='Popup Freq (%)', from_=0, to=100, orient='horizontal', variable=popupVar)
    popupManual = Button(tabGeneral, text='Manual popup...', command=lambda: assign(popupVar, simpledialog.askinteger('Manual Popup', prompt='[0-100]: ')))
    webScale = Scale(tabGeneral, label='Website Freq (%)', from_=0, to=100, orient='horizontal', variable=webVar)
    webManual = Button(tabGeneral, text='Manual web...', command=lambda: assign(webVar, simpledialog.askinteger('Manual Web', prompt='[0-100]: ')))
    audioScale = Scale(tabGeneral, label='Audio Freq (%)', from_=0, to=100, orient='horizontal', variable=audioVar)
    audioManual = Button(tabGeneral, text='Manual audio...', command=lambda: assign(audioVar, simpledialog.askinteger('Manual Audio', prompt='[0-100]: ')))
    promptScale = Scale(tabGeneral, label='Prompt Freq (%)', from_=0, to=100, orient='horizontal', variable=promptVar)
    promptManual = Button(tabGeneral, text='Manual prompt...', command=lambda: assign(promptVar, simpledialog.askinteger('Manual Prompt', prompt='[0-100]: ')))
    mistakeScale = Scale(tabGeneral, label='Prompt Mistakes', from_=0, to=150, orient='horizontal', variable=promptMistakeVar)
    mistakeManual = Button(tabGeneral, text='Manual mistakes...', command=lambda: assign(promptMistakeVar, simpledialog.askinteger('Max Mistakes', prompt='Max mistakes allowed in prompt text\n[0-50]: ')))
        #drive row
    fillBox = Checkbutton(tabGeneral, text='Fill Drive', variable=fillVar, command=lambda: toggleAssociateSettings(fillVar.get(), fill_group))
    fillDelay = Scale(tabGeneral, label='Fill Delay (ms)', from_=0, to=250, orient='horizontal', variable=fillDelayVar)
    
    fill_group.append(fillDelay)
    
    replaceBox = Checkbutton(tabGeneral, text='Replace Images', variable=replaceVar, command=lambda: toggleAssociateSettings(replaceVar.get(), replace_group))
    replaceThreshScale = Scale(tabGeneral, label='Image Threshold', from_=1, to=1000, orient='horizontal', variable=replaceThreshVar)
    
    replace_group.append(replaceThreshScale)

        #other row
    exportResourcesButton = Button(tabGeneral, text='Export resource', command=exportResource)
    importResourcesButton = Button(tabGeneral, text='Import resources', command=lambda: importResource(root))
    toggleStartupButton = Checkbutton(tabGeneral, text='Launch on Startup', variable=startLoginVar)
    toggleDiscordButton = Checkbutton(tabGeneral, text='Show on Discord', variable=discordVar)
    toggleHibernateButton = Checkbutton(tabGeneral, text='Hibernate Mode', variable=hibernateVar, command=lambda: toggleAssociateSettings(hibernateVar.get(), hibernate_group))
    hibernateMinButton = Button(tabGeneral, text='Manual min...', command=lambda: assign(hibernateMinVar, simpledialog.askinteger('Manual Minimum Sleep (sec)', prompt='[1-7200]: ')))
    hibernateMinScale = Scale(tabGeneral, label='Min Sleep (sec)', variable=hibernateMinVar, orient='horizontal', from_=1, to=7200)
    hibernateMaxButton = Button(tabGeneral, text='Manual max...', command=lambda: assign(hibernateMaxVar, simpledialog.askinteger('Manual Maximum Sleep (sec)', prompt='[2-14400]: ')))
    hibernateMaxScale = Scale(tabGeneral, label='Max Sleep (sec)', variable=hibernateMaxVar, orient='horizontal', from_=2, to=14400)
    h_activityScale = Scale(tabGeneral, label='Awaken Activity', orient='horizontal', from_=1, to=50, variable=wakeupActivityVar)
    toggleFlairButton = Checkbutton(tabGeneral, text='Show Loading Flair', variable=startFlairVar)
    toggleCaptionsButton = Checkbutton(tabGeneral, text='Popup Captions', variable=captionVar)
    #zipDropdown = OptionMenu(tabGeneral, zipDropVar, *DOWNLOAD_STRINGS)
    zipLabel = Label(tabGeneral, text='Current Zip:\n' + pickZip(), background='lightgray', wraplength=100)
    #zipDownloadButton = Button(tabGeneral, text='Download Zip', command=lambda: downloadZip(zipDropVar.get(), zipLabel))
    local_verLabel = Label(tabGeneral, text='Local Version:\n' + defaultVars[0])
    web_verLabel = Label(tabGeneral, text='GitHub Version:\n' + webv, bg=('SystemButtonFace' if (defaultVars[0] == webv) else 'red'))
    openGitButton = Button(tabGeneral, text='Open Github', command=lambda: webbrowser.open('https://github.com/PetitTournesol/Edgeware'))
    setPanicButtonButton = Button(tabGeneral, text='Set Panic Button\n' + str(panicButtonVar.get()), command=lambda:getKeyboardInput(setPanicButtonButton, panicButtonVar))
    panicDisableButton = Checkbutton(tabGeneral, text='Disable Panic Hotkey', variable=panicVar)

    hibernate_group.append(h_activityScale)
    hibernate_group.append(hibernateMinButton)
    hibernate_group.append(hibernateMinScale)
    hibernate_group.append(hibernateMaxButton)
    hibernate_group.append(hibernateMaxScale)

    saveExitButton = Button(tabGeneral, text='Save & Exit', command=lambda: write_save(in_var_group, in_var_names))
        #placing
    Label(tabGeneral, text='Annoyance Settings').grid(column=2, row=0)
    Label(tabGeneral, text='Hard Drive Settings').grid(column=2, row=3)
    Label(tabGeneral, text='Other').grid(column=2, row=6)

    delayScale.grid(column=0, row=1)
    delayManual.grid(column=0, row=2)

    popupScale.grid(column=1, row=1)
    popupManual.grid(column=1, row=2)

    webScale.grid(column=2, row=1)
    webManual.grid(column=2, row=2)

    audioScale.grid(column=3, row=1)
    audioManual.grid(column=3, row=2)

    promptScale.grid(column=4, row=1)
    promptManual.grid(column=4, row=2)

    mistakeScale.grid(column=4, row=3)
    mistakeManual.grid(column=4, row=4)

    fillBox.grid(column=0, row=4, sticky='w')
    fillDelay.grid(column=1, row=4)
    replaceBox.grid(column=2, row=4, sticky='w')
    replaceThreshScale.grid(column=3, row=4)

    exportResourcesButton.grid(column=1, row=13)
    importResourcesButton.grid(column=2, row=13)
    panicDisableButton.grid(column=1, row=11, sticky='w')
    setPanicButtonButton.grid(column=1, row=12)
    toggleStartupButton.grid(column=1, row=7, sticky='w')
    toggleDiscordButton.grid(column=1, row=8, sticky='w')

    toggleCaptionsButton.grid(column=0, row=7, sticky='w')
    toggleHibernateButton.grid(column=2,row=8,padx=5,pady=2, sticky='w')
    h_activityScale.grid(column=2, row=7)
    hibernateMinScale.grid(column=3,row=7,padx=5,pady=2)
    hibernateMaxScale.grid(column=4,row=7,padx=5,pady=2)
    hibernateMinButton.grid(column=3,row=8,padx=5,pady=2)
    hibernateMaxButton.grid(column=4,row=8,padx=5,pady=2)
    
    #zipDownloadButton.grid(column=0, row=10) #not using for now until can find consistent direct download
    #zipDropdown.grid(column=0, row=9)
    zipLabel.grid(column=0, row=10)
    toggleFlairButton.grid(column=0,row=8, sticky='w')
    local_verLabel.grid(column=0, row=11)
    web_verLabel.grid(column=0, row=12)
    openGitButton.grid(column=0, row=13)

    Label(tabGeneral).grid(column=4, row=9)
    Label(tabGeneral).grid(column=4, row=10)
    Label(tabGeneral).grid(column=4, row=11)
    saveExitButton.grid(column=4, row=13)
    #==========={HERE ENDS  GENERAL TAB ITEM INITS}===========#
    tabMaster.add(tabAdvanced, text='Advanced')
    #==========={IN HERE IS ADVANCED TAB ITEM INITS}===========#
    itemList = []
    for obj in settingJsonObj:
        itemList.append(obj)
    dropdownObj = StringVar(root, itemList[0])
    textObj = StringVar(root, settingJsonObj[dropdownObj.get()])
    textInput = Entry(tabAdvanced)
    textInput.insert(1, textObj.get())
    expectedLabel = Label(tabAdvanced, text='Expected value: ' + str(defaultJsonObj[dropdownObj.get()]))
    dropdownMenu = OptionMenu(tabAdvanced, dropdownObj, *itemList, command=lambda a: updateText([textInput, expectedLabel], settingJsonObj[a], a))
    dropdownMenu.configure(width=10)
    applyButton = Button(tabAdvanced, text='Apply', command= lambda: assignJSON(dropdownObj.get(), textInput.get()))
    Label(tabAdvanced, text='Be careful messing with some of these; improper configuring can cause\nproblems when running, or potentially cause unintended damage to files.').grid(column=3, row=1)
    Label(tabAdvanced).grid(column=1, row=1)
    Label(tabAdvanced).grid(column=0, row=1)
    dropdownMenu.grid(column=2, row=2)
    textInput.grid(column=3, row=2, ipadx=110)
    applyButton.grid(column=4, row=2)
    expectedLabel.grid(column=3, row=3)
    #==========={HERE ENDS  ADVANCED TAB ITEM INITS}===========#
    tabMaster.add(tabInfo, text='About')
    #==========={IN HERE IS ABOUT TAB ITEM INITS}===========#
    tabInfoExpound.add(tab_annoyance, text='Annoyance')
    Label(tab_annoyance, text=ANNOYANCE_TEXT, anchor='nw', wraplength=460).pack()
    tabInfoExpound.add(tab_drive, text='Hard Drive')
    Label(tab_drive, text=DRIVE_TEXT, anchor='nw', wraplength=460).pack()
    #tabInfoExpound.add(tab_export, text='Exporting')
    tabInfoExpound.add(tab_launch, text='Startup')
    Label(tab_launch, text=STARTUP_TEXT, anchor='nw', wraplength=460).pack()
    tabInfoExpound.add(tab_hibernate, text='Hibernate')
    Label(tab_hibernate, text=HIBERNATE_TEXT, anchor='nw', wraplength=460).pack()
    tabInfoExpound.add(tab_advanced, text='Advanced')
    Label(tab_advanced, text=ADVANCED_TEXT, anchor='nw', wraplength=460).pack()
    tabInfoExpound.add(tab_thanksAndAbout, text='Thanks & About')
    Label(tab_thanksAndAbout, text=THANK_AND_ABOUT_TEXT, anchor='nw', wraplength=460).pack()
    #==========={HERE ENDS  ABOUT TAB ITEM INITS}===========#

    toggleAssociateSettings(fillVar.get(), fill_group)
    toggleAssociateSettings(replaceVar.get(), replace_group)
    toggleAssociateSettings(hibernateVar.get(), hibernate_group)
    
    tabMaster.pack(expand=1, fill='both')
    tabInfoExpound.pack(expand=1, fill='both')

    if not settingJsonObj['is_configed'] == 1: 
        messagebox.showinfo('First Config', 'Config has not been run before. All settings are defaulted to frequency of 0.\n[This alert will only appear on the first run of config]')
    if local_version != webv:
        messagebox.showwarning('Update Available', 'Local version and web version are not the same.\nThis likely means a newer version is available.')

    root.mainloop()

def pickZip():
    #selecting zip
    for obj in os.listdir(PATH + '\\'):
        try:
            if obj.split('.')[len(obj.split('.'))-1].lower() == 'zip':
                return obj.split('.')[0]
        except:
            print('{} is not a zip file.'.format(obj))
    return '[No Zip Found]'

def exportResource():
    try:
        saveLocation = filedialog.asksaveasfile('w', defaultextension ='.zip')
        with zipfile.ZipFile(saveLocation.name, 'w', compression=zipfile.ZIP_DEFLATED) as zip:
            beyondRoot = False
            for root, dirs, files in os.walk(os.path.join(PATH, 'resource')):
                for obj in files:
                    if beyondRoot:
                        zip.write(os.path.join(root, obj), root.split('\\')[len(root.split('\\')) - 1] + '\\' + obj)
                    else:
                        zip.write(os.path.join(root, obj), '\\' + obj)
                for dir in dirs:
                    zip.write(os.path.join(root, dir), '\\' + dir + '\\')
                beyondRoot = True
    except:
        messagebox.showerror('Write Error', 'Failed to export resource to zip file.')

def importResource(parent):
    try:
        openLocation = filedialog.askopenfile('r', defaultextension ='.zip')
        if openLocation == None:
            return False
        if os.path.exists(PATH + 'resource\\'):
            resp = confirmBox(parent)
            if not resp:
                return False
            shutil.rmtree(PATH + 'resource\\')
        with zipfile.ZipFile(openLocation.name, 'r') as zip:
            zip.extractall(PATH + 'resource\\')
        messagebox.showinfo('Done', 'Resource importing completed.')
    except Exception as e:
        messagebox.showerror('Read Error', 'Failed to import resources from file.\n[' + str(e) + ']')

def confirmBox(parent) -> bool:
    allow = False
    root = Toplevel(parent)
    def complete(state):
        nonlocal allow
        allow=state
        root.quit()
    root.geometry('220x120')
    root.resizable(False, False)
    root.wm_attributes('-toolwindow', 1)
    root.focus_force()
    root.title('Confirm')
    Label(root, text='Current resource folder will be deleted and overwritten. Is this okay?', wraplength=212).pack(fill='x')
    Label(root).pack()
    Button(root, text='Continue', command=lambda: complete(True)).pack()
    Button(root, text='Cancel', command=lambda: complete(False)).pack()
    root.mainloop()
    try:
        root.destroy()
    except:
        False
    return allow

#helper funcs for lambdas =======================================================

def write_save(varList, nameList):
    temp = json.loads('{}')
    settingJsonObj['is_configed'] = 1
    #, command=lambda: toggleStartupBat(startLoginVar.get())
    toggleStartupBat(varList[nameList.index('start_on_logon')].get())
    for name in varNames:
        try:
            p = varList[nameList.index(name)].get()
            temp[name] = p if type(p) is int else (1 if type(p) is bool and p else 0)
        except:
            temp[name] = settingJsonObj[name]
    with open(PATH + 'config.cfg', 'w') as file:
        file.write(json.dumps(temp))
    os.kill(os.getpid(), 9)

#def downloadZip(str, lblObj):
#    url = URL_BASE + DOWNLOAD_LINKS[DOWNLOAD_STRINGS.index(str)]
#    print('downloading zip from:', url)
#    with urllib.request.urlopen(url) as file, open(PATH + str + '.zip', 'wb') as out:
#        shutil.copyfileobj(file, out)

def getLiveVersion():
    try:
        with open(urllib.request.urlretrieve(UPDCHECK_URL)[0], 'r') as liveDCfg:
            return(liveDCfg.read().split('\n')[1].split(',')[0])
    except:
        return 'Could not check version.'
    

def updateText(objList, var, var_Label):
    try:
        for obj in objList:
            if type(obj) == Entry:
                obj.delete(0, 9999)
                obj.insert(1, var)
            elif type(obj) == Label:
                obj.configure(text='Expected value: ' + str(defaultJsonObj[var_Label]))
    except:
        print('idk what would cause this but just in case uwu')

def assignJSON(key, var):
    settingJsonObj[key] = var
    with open(PATH + 'config.cfg', 'w') as f:
        f.write(json.dumps(settingJsonObj))
    
def toggleAssociateSettings(ownerState, objList):
    for obj in objList:
        obj.configure(state=('normal' if ownerState else 'disabled'))
        obj.configure(bg=('SystemButtonFace' if ownerState else 'gray25'))

def toggleStartupBat(boolean):
    try:
        if boolean:
            with open(os.path.expanduser('~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\edgeware.bat'), 'w') as file:
                file.write('@echo off\ncd ' + PATH + '\npython ' + PATH + 'p_start.pyw')
        else:
            os.remove(os.path.expanduser('~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\edgeware.bat'))
    except:
        print('uwu')

def assign(obj, var):
    try:
        obj.set(var)
    except:
        print('Should silently fail; did user quit out of input without submitting?')

def getKeyboardInput(button, var):
    child = Tk()
    child.resizable(False,False)
    child.title('Key Listener')
    child.wm_attributes('-topmost', 1)
    child.geometry('250x250')
    child.focus_force()
    Label(child, text='Press any key or exit').pack(expand=1, fill='both')
    child.bind('<KeyPress>', lambda key: assignKey(child, button, var, key))
    child.mainloop()

def assignKey(parent, button, var, key):
    button.configure(text='Set Panic Button\n<' + key.keysym + '>')
    var.set(str(key.keycode))
    parent.destroy()

try:
    spawnWindow()
except Exception as e:
    messagebox.showerror('Could not start', 'Could not start config.\n[' + str(e) + ']')
