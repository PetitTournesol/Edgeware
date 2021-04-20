import json, os, shutil, webbrowser, zipfile, pathlib, ast, requests, urllib.request 
from tkinter import Tk, ttk, simpledialog, messagebox, filedialog
from tkinter import *

PATH = str(pathlib.Path(__file__).parent.absolute()) + '\\'
os.chdir(PATH)

#text for the about tab
ANNOYANCE_TEXT = 'The "Annoyance" section consists of the 5 main configurable settings of Edgeware:\nDelay\nPopup Frequency\nWebsite Frequency\nAudio Frequency\nPromptFrequency\n\nEach is fairly self explanatory, but will still be expounded upon in this section. Delay is the forced time delay between each tick of the "clock" for Edgeware. The longer it is, the slower things will happen. Popup frequency is the percent chance that a randomly selected popup will appear on any given tick of the clock, and similarly for the rest, website being the probability of opening a website or video from /resource/vid/, audio for playing a file from /resource/aud/, and prompt for a typing prompt to pop up.\n\nThese values can be set by adjusting the bars, or by clicking the button beneath each respective slider, which will allow you to type in an explicit number instead of searching for it on the scrollbar.\n\nIn order to disable any feature, lower its probability to 0, to ensure that you\'ll be getting as much of any feature as possible, turn it up to 100.\nThe popup setting "Mitosis mode" changes how popups are displayed. Instead of popping up based on the timer, the program create a single popup when it starts. When the submit button on ANY popup is clicked to close it, a number of popups will open up in its place, as given by the "Mitosis Strength" setting.\n\nPopup timeout will result in popups timing out and closing after a certain number of seconds.'
DRIVE_TEXT = 'The "Drive" portion of Edgeware has three features: fill drive, replace images, and Booru downloader.\n\n"Fill Drive" does exactly what it says: it attempts to fill your hard drive with as much porn from /resource/img/ as possible. It does, however, have some restrictions. It will (should) not place ANY images into folders that start with a "." or have their names listed in the folder name blacklist.\nIt will also ONLY place images into the User folder and its subfolders.\nFill drive has one modifier, which is its own forced delay. Because it runs with between 1 and 8 threads at any given time, when unchecked it can fill your drive VERY quickly. To ensure that you get that nice slow fill, you can adjust the delay between each folder sweep it performs and the max number of threads.\n\n"Replace Images" is more complicated. Its searching is the exact same as fill drive, but instead of throwing images everywhere, it will seek out folders with large numbers of images (more than the threshold value) and when it finds one, it will replace ALL of the images with porn from /resource/img/. REMEMBER THAT IF YOU CARE ABOUT YOUR PHOTOS, AND THEY\'RE IN A FOLDER WITH MORE IMAGES THAN YOUR CHOSEN THRESHOLD VALUE, EITHER BACK THEM UP IN A ZIP OR SOMETHING OR DO. NOT. USE. THIS SETTING. I AM NOT RESPONSIBLE FOR YOUR OWN DECISION TO RUIN YOUR PHOTOS.\n\nBooru downloader allows you to download new items from a Booru of your choice. For the booru name, ONLY the literal name is used, like "censored" or "blacked" instead of the full url. This is not case sensitive. Use the "Validate" button to ensure that downloading will be successful before running. For tagging, if you want to have mutliple tags, they can be combined using "tag1+tag2+tag3" or if you want to add blacklist tags, type your tag and append a "+-blacklist_tag" after the desired tag.'
STARTUP_TEXT = 'Start on launch does exactly what it says it does and nothing more: it allows Edgeware to start itself whenever you start up and log into your PC.\n\nPlease note that the method used does NOT edit registry or schedule any tasks. The "lazy startup" method was used for both convenience of implementation and convenience of cleaning.\n\nIf you forget to turn off the "start on logon" setting before uninstalling, you will need to manually go to your Startup folder and remove "edgeware.bat".'
WALLPAPER_TEXT = 'The Wallpaper section allows you to set up rotating wallpapers of your choice from any location, or auto import all images from the /resource/ folder (NOT /resource/img/ folder) to use as wallpapers.\n\nThe rotate timer is the amount of time the program will wait before rotating to another randomly selected wallpaper, and the rotate variation is the amount above or below that set value that can randomly be selected as the actual wait time.'
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

BOORU_FLAG = '<BOORU_INSERT>'
BOORU_URL  = 'https://' + BOORU_FLAG + '.booru.org/index.php?page=post&s=list&tags='
BOORU_VIEW = 'https://' + BOORU_FLAG + '.booru.org/index.php?page=post&s=view&id='
BOORU_PTAG = '&pid='

UPDCHECK_URL = 'http://raw.githubusercontent.com/PetitTournesol/Edgeware/main/EdgeWare/configDefault.dat'
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

DEFAULT_WALLPAPERDAT = {"default": (PATH.replace('\\', '/') + "resource/wallpaper.png")}
if settingJsonObj['wallpaperDat'] == 'WPAPER_DEF':
    settingJsonObj['wallpaperDat'] = DEFAULT_WALLPAPERDAT
else:
    settingJsonObj['wallpaperDat'] = ast.literal_eval(settingJsonObj['wallpaperDat'])

def spawnWindow():
    global settingJsonObj, defaultJsonObj
    webv = getLiveVersion()

    #window things
    root = Tk()
    root.title('Edgeware Config')
    root.geometry('740x620')
    root.iconbitmap(PATH + 'default_assets\\config_icon.ico')
    fail_loop = 0

    #painful control variables ._.
    while(fail_loop < 2):
        try:
            delayVar            = IntVar(root, value=int(settingJsonObj['delay']))
            popupVar            = IntVar(root, value=int(settingJsonObj['popupMod']))
            webVar              = IntVar(root, value=int(settingJsonObj['webMod']))
            audioVar            = IntVar(root, value=int(settingJsonObj['audioMod']))
            promptVar           = IntVar(root, value=int(settingJsonObj['promptMod']))
            fillVar             = BooleanVar(root, value=(settingJsonObj['fill']==1))

            fillDelayVar        = IntVar(root, value=int(settingJsonObj['fill_delay']))
            replaceVar          = BooleanVar(root, value=(settingJsonObj['replace'] == 1))
            replaceThreshVar    = IntVar(root, value=int(settingJsonObj['replaceThresh']))
            startLoginVar       = BooleanVar(root, value=(settingJsonObj['start_on_logon'] == 1))

            hibernateVar        = BooleanVar(root, value=(settingJsonObj['hibernateMode']==1))
            hibernateMinVar     = IntVar(root, value=int(settingJsonObj['hibernateMin']))
            hibernateMaxVar     = IntVar(root, value=(settingJsonObj['hibernateMax']))
            wakeupActivityVar   = IntVar(root, value=(settingJsonObj['wakeupActivity']))

            discordVar          = BooleanVar(root, value=(int(settingJsonObj['showDiscord'])==1))
            startFlairVar       = BooleanVar(root, value=(int(settingJsonObj['showLoadingFlair'])==1))
            captionVar          = BooleanVar(root, value=(int(settingJsonObj['showCaptions'])==1))
            panicButtonVar      = StringVar(root, value=settingJsonObj['panicButton'])
            panicVar            = BooleanVar(root, value=(int(settingJsonObj['panicDisabled'])==1))

            promptMistakeVar    = IntVar(root, value=int(settingJsonObj['promptMistakes']))
            mitosisVar          = BooleanVar(root, value=(int(settingJsonObj['mitosisMode'])==1))
            onlyVidVar          = BooleanVar(root, value=(int(settingJsonObj['onlyVid'])==1))
            popupWebVar         = BooleanVar(root, value=(int(settingJsonObj['webPopup'])==1))

            rotateWallpaperVar  = BooleanVar(root, value=(int(settingJsonObj['rotateWallpaper'])==1))
            wallpaperDelayVar   = IntVar(root, value=int(settingJsonObj['wallpaperTimer']))
            wpVarianceVar       = IntVar(root, value=int(settingJsonObj['wallpaperVariance']))

            timeoutPopupsVar    = BooleanVar(root, value=(int(settingJsonObj['timeoutPopups'])==1))
            popupTimeoutVar     = IntVar(root, value=(int(settingJsonObj['popupTimeout'])))
            mitosisStrenVar     = IntVar(root, value=(int(settingJsonObj['mitosisStrength'])))
            booruNameVar        = StringVar(root, value=settingJsonObj['booruName'])
            
            downloadEnabledVar  = BooleanVar(root, value=(int(settingJsonObj['downloadEnabled']) == 1))
            downloadModeVar     = StringVar(root, value=settingJsonObj['downloadMode'])
            useWebResourceVar   = BooleanVar(root, value=(int(settingJsonObj['useWebResource'])==1))
            fillPathVar         = StringVar(root, value=settingJsonObj['drivePath'])
            
            #grouping for sanity's sake later
            in_var_group = [delayVar, popupVar, webVar, audioVar, promptVar, fillVar, 
                            fillDelayVar, replaceVar, replaceThreshVar, startLoginVar, 
                            hibernateVar, hibernateMinVar, hibernateMaxVar, wakeupActivityVar, 
                            discordVar, startFlairVar, captionVar, panicButtonVar, panicVar, 
                            promptMistakeVar, mitosisVar, onlyVidVar, popupWebVar,
                            rotateWallpaperVar, wallpaperDelayVar, wpVarianceVar,
                            timeoutPopupsVar, popupTimeoutVar, mitosisStrenVar, booruNameVar,
                            downloadEnabledVar, downloadModeVar, useWebResourceVar, fillPathVar]

            in_var_names = ['delay', 'popupMod', 'webMod', 'audioMod', 'promptMod', 'fill', 
                            'fill_delay', 'replace', 'replaceThresh', 'start_on_logon', 
                            'hibernateMode', 'hibernateMin', 'hibernateMax', 'wakeupActivity', 
                            'showDiscord', 'showLoadingFlair', 'showCaptions', 'panicButton', 'panicDisabled',
                            'promptMistakes', 'mitosisMode', 'onlyVid', 'webPopup',
                            'rotateWallpaper', 'wallpaperTimer', 'wallpaperVariance',
                            'timeoutPopups', 'popupTimeout', 'mitosisStrength', 'booruName',
                            'downloadEnabled', 'downloadMode', 'useWebResource', 'drivePath']
            break
        except Exception as e:
            messagebox.showwarning(
                        'Settings Warning', 
                        'File "config.cfg" appears corrupted.\nFile will be restored to default.\n[' + str(e) + ']'
                        )
            jObj = {}
            for var in varNames:
                jObj[var] = defaultVars[varNames.index(var)]
            with open(PATH + 'config.cfg', 'w') as f:
                f.write(json.dumps(jObj))
            with open(PATH + 'config.cfg', 'r') as f:
                settingJsonObj = json.loads(f.readline())
            fail_loop += 1

    hasWebResourceVar = BooleanVar(root, os.path.exists(os.path.join(PATH, 'resource', 'webResource.json')))

    #done painful control variables

    #grouping for enable/disable
    hibernate_group = []
    fill_group      = []
    replace_group   = []
    mitosis_group   = []
    mitosis_cGroup  = []
    wallpaper_group = []
    timeout_group   = []
    download_group  = []

    #tab display code start
    tabMaster    = ttk.Notebook(root)       #tab manager
    tabGeneral   = ttk.Frame(None)          #general tab, will have current settings
    tabWallpaper = ttk.Frame(None)          #tab for wallpaper rotation settings
    tabAnnoyance = ttk.Frame(None)          #tab for popup settings
    tabDrive     = ttk.Frame(None)          #tab for drive settings
    tabJSON      = ttk.Frame(None)          #tab for JSON editor (unused)
    tabAdvanced  = ttk.Frame(None)          #advanced tab, will have settings pertaining to startup, hibernation mode settings
    tabInfo      = ttk.Frame(None)          #info, github, version, about, etc.

    style = ttk.Style(root)                 #style setting for left aligned tabs
    style.configure('lefttab.TNotebook', tabposition='wn')
    tabInfoExpound = ttk.Notebook(tabInfo, style='lefttab.TNotebook')  #additional subtabs for info on features

    tab_annoyance = ttk.Frame(None)
    tab_drive = ttk.Frame(None)
    tab_wallpaper = ttk.Frame(None)
    tab_launch = ttk.Frame(None)
    tab_hibernate = ttk.Frame(None)
    tab_advanced = ttk.Frame(None)
    tab_thanksAndAbout = ttk.Frame(None)

    tabMaster.add(tabGeneral, text='General')
    #==========={IN HERE IS GENERAL TAB ITEM INITS}===========#
    #init
    hibernateHostFrame = Frame(tabGeneral, borderwidth=5, relief=RAISED)
    hibernateFrame = Frame(hibernateHostFrame)
    hibernateMinFrame = Frame(hibernateHostFrame)
    hibernateMaxFrame = Frame(hibernateHostFrame)

    toggleHibernateButton = Checkbutton(hibernateHostFrame, text='Hibernate Mode', variable=hibernateVar, command=lambda: toggleAssociateSettings(hibernateVar.get(), hibernate_group))
    hibernateMinButton = Button(hibernateMinFrame, text='Manual min...', command=lambda: assign(hibernateMinVar, simpledialog.askinteger('Manual Minimum Sleep (sec)', prompt='[1-7200]: ')))
    hibernateMinScale = Scale(hibernateMinFrame, label='Min Sleep (sec)', variable=hibernateMinVar, orient='horizontal', from_=1, to=7200)
    hibernateMaxButton = Button(hibernateMaxFrame, text='Manual max...', command=lambda: assign(hibernateMaxVar, simpledialog.askinteger('Manual Maximum Sleep (sec)', prompt='[2-14400]: ')))
    hibernateMaxScale = Scale(hibernateMaxFrame, label='Max Sleep (sec)', variable=hibernateMaxVar, orient='horizontal', from_=2, to=14400)
    h_activityScale = Scale(hibernateHostFrame, label='Awaken Activity', orient='horizontal', from_=1, to=50, variable=wakeupActivityVar)
        
    hibernate_group.append(h_activityScale)
    hibernate_group.append(hibernateMinButton)
    hibernate_group.append(hibernateMinScale)
    hibernate_group.append(hibernateMaxButton)
    hibernate_group.append(hibernateMaxScale)
    
    Label(tabGeneral, text='Hibernate Settings').pack()
    hibernateHostFrame.pack(fill='x')
    hibernateFrame.pack(fill='y', side='left')
    toggleHibernateButton.pack(fill='x', side='left')
    hibernateMinFrame.pack(fill='y', side='left')
    hibernateMinScale.pack(fill='y')
    hibernateMinButton.pack(fill='y')
    hibernateMaxScale.pack(fill='y')
    hibernateMaxButton.pack(fill='y')
    hibernateMaxFrame.pack(fill='x', side='left')
    h_activityScale.pack(fill='y', side='left')

    #other
    Label(tabGeneral, text='Other').pack()
    otherHostFrame = Frame(tabGeneral, borderwidth=5, relief=RAISED)
    resourceFrame = Frame(otherHostFrame)
    exportResourcesButton = Button(resourceFrame, text='Export resource', command=exportResource)
    importResourcesButton = Button(resourceFrame, text='Import resources', command=lambda: importResource(root))
    toggleFrame1 = Frame(otherHostFrame)
    toggleFrame2 = Frame(otherHostFrame)

    toggleStartupButton = Checkbutton(toggleFrame1, text='Launch on Startup', variable=startLoginVar)
    toggleDiscordButton = Checkbutton(toggleFrame1, text='Show on Discord', variable=discordVar)
    toggleFlairButton = Checkbutton(toggleFrame2, text='Show Loading Flair', variable=startFlairVar)

    otherHostFrame.pack(fill='x')
    resourceFrame.pack(fill='y', side='left')
    exportResourcesButton.pack(fill='x')
    importResourcesButton.pack(fill='x')
    toggleFrame1.pack(fill='y', side='left')
    toggleStartupButton.pack(fill='x')
    toggleDiscordButton.pack(fill='x')
    toggleFrame2.pack(fill='y', side='left')
    toggleFlairButton.pack(fill='x')

    Label(tabGeneral, text='Information').pack()
    infoHostFrame = Frame(tabGeneral, borderwidth=5, relief=RAISED)
    zipGitFrame = Frame(infoHostFrame)
    verFrame = Frame(infoHostFrame)
    #zipDropdown = OptionMenu(tabGeneral, zipDropVar, *DOWNLOAD_STRINGS)
    #zipDownloadButton = Button(tabGeneral, text='Download Zip', command=lambda: downloadZip(zipDropVar.get(), zipLabel))
    zipLabel = Label(zipGitFrame, text='Current Zip:\n' + pickZip(), background='lightgray', wraplength=100)
    local_verLabel = Label(verFrame, text='Local Version:\n' + defaultVars[0])
    web_verLabel = Label(verFrame, text='GitHub Version:\n' + webv, bg=('SystemButtonFace' if (defaultVars[0] == webv) else 'red'))
    openGitButton = Button(zipGitFrame, text='Open Github', command=lambda: webbrowser.open('https://github.com/PetitTournesol/Edgeware'))

    infoHostFrame.pack(fill='x')
    zipGitFrame.pack(fill='y', side='left')
    zipLabel.pack(fill='x')
    openGitButton.pack(fill='x')
    verFrame.pack(fill='y', side='left')
    local_verLabel.pack(fill='x')
    web_verLabel.pack(fill='x')

    forceReload = Button(infoHostFrame, text='Force Reload', command=refresh)

    saveExitButton = Button(root, text='Save & Exit', command=lambda: write_save(in_var_group, in_var_names))

    #force reload button for debugging, only appears on DEV versions
    if local_version.endswith('DEV'):
        forceReload.pack(fill='x')
    
    #zipDownloadButton.grid(column=0, row=10) #not using for now until can find consistent direct download
    #zipDropdown.grid(column=0, row=9)
    #==========={HERE ENDS  GENERAL TAB ITEM INITS}===========#
    tabMaster.add(tabAnnoyance, text='Annoyance')

    Label(tabAnnoyance).pack()

    delayScale = Scale(tabAnnoyance, label='Timer Delay (ms)', from_=10, to=60000, orient='horizontal', variable=delayVar)
    delayManual = Button(tabAnnoyance, text='Manual delay...', command=lambda: assign(delayVar, simpledialog.askinteger('Manual Delay', prompt='[10-60000]: ')))

    delayScale.pack(fill='x')
    delayManual.pack(fill='x')
    #popup frame handling
    popupHostFrame = Frame(tabAnnoyance, borderwidth=5, relief=RAISED)
    popupFrame = Frame(popupHostFrame)
    timeoutFrame = Frame(popupHostFrame)
    mitosisFrame = Frame(popupHostFrame)
    
    popupScale = Scale(popupFrame, label='Popup Freq (%)', from_=0, to=100, orient='horizontal', variable=popupVar)
    popupManual = Button(popupFrame, text='Manual popup...', command=lambda: assign(popupVar, simpledialog.askinteger('Manual Popup', prompt='[0-100]: ')))

    mitosis_group.append(popupScale)
    mitosis_group.append(popupManual)

    def toggleMitosis():
        toggleAssociateSettings(not mitosisVar.get(), mitosis_group)
        toggleAssociateSettings(mitosisVar.get(), mitosis_cGroup)

    mitosisToggle = Checkbutton(mitosisFrame, text='Mitosis Mode', variable=mitosisVar, command=toggleMitosis)
    mitosisStren  = Scale(mitosisFrame, label='Mitosis Strength', orient='horizontal', from_=2, to=10, variable=mitosisStrenVar)

    mitosis_cGroup.append(mitosisStren)

    panicFrame = Frame(popupHostFrame)
    setPanicButtonButton = Button(panicFrame, text='Set Panic Button\n<' + str(panicButtonVar.get()) + '>', command=lambda:getKeyboardInput(setPanicButtonButton, panicButtonVar))
    doPanicButton = Button(panicFrame, text='Perform Panic', command=lambda: os.startfile('panic.pyw'))
    panicDisableButton = Checkbutton(popupHostFrame, text='Disable Panic Hotkey', variable=panicVar)

    popupWebToggle= Checkbutton(popupHostFrame, text='Popup close opens web page', variable=popupWebVar)
    toggleCaptionsButton = Checkbutton(popupHostFrame, text='Popup Captions', variable=captionVar)

    timeoutToggle = Checkbutton(timeoutFrame, text='Popup Timeout', variable=timeoutPopupsVar, command=lambda: toggleAssociateSettings(timeoutPopupsVar.get(), timeout_group))
    timeoutSlider = Scale(timeoutFrame, label='Time (sec)', from_=1, to=120, orient='horizontal', variable=popupTimeoutVar)

    timeout_group.append(timeoutSlider)

    popupHostFrame.pack(fill='x')
    popupScale.pack(fill='x')
    popupManual.pack(fill='x')
    popupFrame.pack(fill='y', side='left')
    timeoutSlider.pack(fill='x')
    timeoutToggle.pack(fill='x')
    timeoutFrame.pack(fill='y', side='left')
    mitosisFrame.pack(fill='y', side='left')
    mitosisStren.pack(fill='x')
    mitosisToggle.pack(fill='x')
    panicFrame.pack(fill='y', side='left')
    setPanicButtonButton.pack(fill='x')
    doPanicButton.pack(fill='x')
    panicDisableButton.pack(fill='x')
    popupWebToggle.pack(fill='x')
    toggleCaptionsButton.pack(fill='x')
    #popup frame handle end
    
    #audio frame handle start
    audioHostFrame = Frame(tabAnnoyance, borderwidth=5, relief=RAISED)
    audioFrame = Frame(audioHostFrame)

    audioScale = Scale(audioFrame, label='Audio Freq (%)', from_=0, to=100, orient='horizontal', variable=audioVar)
    audioManual = Button(audioFrame, text='Manual audio...', command=lambda: assign(audioVar, simpledialog.askinteger('Manual Audio', prompt='[0-100]: ')))
    
    audioHostFrame.pack(fill='x')
    audioScale.pack(fill='x')
    audioManual.pack(fill='x')
    audioFrame.pack(side='left')
    #audio frame handle end

    #prompt fram handle start
    promptHostFrame = Frame(tabAnnoyance, borderwidth=5, relief=RAISED)
    promptFrame = Frame(promptHostFrame)
    mistakeFrame = Frame(promptHostFrame)

    promptScale = Scale(promptFrame, label='Prompt Freq (%)', from_=0, to=100, orient='horizontal', variable=promptVar)
    promptManual = Button(promptFrame, text='Manual prompt...', command=lambda: assign(promptVar, simpledialog.askinteger('Manual Prompt', prompt='[0-100]: ')))
    
    mistakeScale = Scale(mistakeFrame, label='Prompt Mistakes', from_=0, to=150, orient='horizontal', variable=promptMistakeVar)
    mistakeManual = Button(mistakeFrame, text='Manual mistakes...', command=lambda: assign(promptMistakeVar, simpledialog.askinteger('Max Mistakes', prompt='Max mistakes allowed in prompt text\n[0-150]: ')))
    
    promptHostFrame.pack(fill='x')
    promptFrame.pack(fill='y', side='left')
    promptScale.pack(fill='x')
    promptManual.pack(fill='x')
    mistakeFrame.pack(fill='y', side='left')
    mistakeScale.pack(fill='x')
    mistakeManual.pack(fill='x')
    #prompt end

    #web start
    webHostFrame = Frame(tabAnnoyance, borderwidth=5, relief=RAISED)
    webFrame = Frame(webHostFrame)

    webScale = Scale(webFrame, label='Website Freq (%)', from_=0, to=100, orient='horizontal', variable=webVar)
    webManual = Button(webFrame, text='Manual web...', command=lambda: assign(webVar, simpledialog.askinteger('Manual Web', prompt='[0-100]: ')))

    onlyVidToggle = Checkbutton(webHostFrame, text='Only Vids', variable=onlyVidVar)
    
    webHostFrame.pack(fill='x')
    webFrame.pack(fill='y', side='left')
    webScale.pack(fill='x')
    webManual.pack(fill='x')

    onlyVidToggle.pack(fill='x')
    #end web
    #===================={DRIVE}==============================#
    tabMaster.add(tabDrive, text='Drive')

    hardDriveFrame = Frame(tabDrive, borderwidth=5, relief=RAISED)

    pathFrame = Frame(hardDriveFrame)
    fillFrame = Frame(hardDriveFrame)
    replaceFrame = Frame(hardDriveFrame)

    def local_assignPath():
        nonlocal fillPathVar
        path_ = str(filedialog.askdirectory(initialdir='/', title='Select Parent Folder'))
        if(path_ != ''):
            settingJsonObj['drivePath'] = path_
            pathBox.configure(state='normal')
            pathBox.delete(0, 9999)
            pathBox.insert(1, path_)
            pathBox.configure(state='disabled')
            fillPathVar.set(str(pathBox.get()))
    pathBox = Entry(pathFrame)
    pathButton = Button(pathFrame, text='Select', command=local_assignPath)

    pathBox.insert(1, settingJsonObj['drivePath'])
    pathBox.configure(state='disabled')

    fillBox = Checkbutton(fillFrame, text='Fill Drive', variable=fillVar, command=lambda: toggleAssociateSettings(fillVar.get(), fill_group))
    fillDelay = Scale(fillFrame, label='Fill Delay (ms)', from_=0, to=250, orient='horizontal', variable=fillDelayVar)
    
    fill_group.append(fillDelay)
    
    replaceBox = Checkbutton(fillFrame, text='Replace Images', variable=replaceVar, command=lambda: toggleAssociateSettings(replaceVar.get(), replace_group))
    replaceThreshScale = Scale(fillFrame, label='Image Threshold', from_=1, to=1000, orient='horizontal', variable=replaceThreshVar)
    
    replace_group.append(replaceThreshScale)

    avoidHostFrame = Frame(hardDriveFrame)

    avoidListBox = Listbox(avoidHostFrame, selectmode=SINGLE)
    for name in settingJsonObj['avoidList'].split('>'):
        avoidListBox.insert(2, name)
    addName = Button(avoidHostFrame, text='Add Name', command=lambda: addList(avoidListBox, 'avoidList', 'Folder Name', 'Fill/replace will skip any folder with given name.'))
    removeName = Button(avoidHostFrame, text='Remove Name', command=lambda: removeList(avoidListBox, 'avoidList', 'Remove EdgeWare', 'You cannot remove the EdgeWare folder exception.'))
    resetName  = Button(avoidHostFrame, text='Reset', command=lambda: resetList(avoidListBox, 'avoidList', 'EdgeWare>AppData'))

    avoidHostFrame.pack(fill='y', side='left') 
    Label(avoidHostFrame, text='Folder Name Blacklist').pack(fill='x')
    avoidListBox.pack(fill='x')
    addName.pack(fill='x')
    removeName.pack(fill='x')
    resetName.pack(fill='x')

    Label(tabDrive, text='Hard Drive Settings').pack(fill='both')
    hardDriveFrame.pack(fill='x')
    fillFrame.pack(fill='y', side='left')
    fillBox.pack()
    fillDelay.pack()
    replaceFrame.pack(fill='y', side='left')
    replaceBox.pack()
    replaceThreshScale.pack()
    pathFrame.pack(fill='x')
    Label(pathFrame, text='Fill/Replace Start Folder').pack(fill='x')
    pathBox.pack(fill='x')
    pathButton.pack(fill='x')

    downloadHostFrame = Frame(tabDrive, borderwidth=5, relief=RAISED)
    otherFrame = Frame(downloadHostFrame)
    tagFrame   = Frame(downloadHostFrame)
    booruFrame = Frame(downloadHostFrame)
    booruNameEntry = Entry(booruFrame, textvariable=booruNameVar)
    downloadEnabled = Checkbutton(otherFrame, text='Download from Booru', variable=downloadEnabledVar, command=lambda: (
        toggleAssociateSettings_manual(downloadEnabledVar.get(), download_group, 'white', 'gray25')))
    downloadResourceEnabled = Checkbutton(otherFrame, text='Download from webResource', variable=useWebResourceVar)
    toggleAssociateSettings(hasWebResourceVar.get(), [downloadResourceEnabled])
    downloadMode    = OptionMenu(booruFrame, downloadModeVar, *['All', 'First Page', 'Random Page'])
    downloadMode.configure(width=15)
    booruValidate  = Button(booruFrame, text='Validate', command=lambda: (
        messagebox.showinfo('Success!', 'Booru is valid.') 
        if validateBooru(booruNameVar.get()) else 
        messagebox.showerror('Failed', 'Booru is invalid.')
    ))

    tagListBox = Listbox(tagFrame, selectmode=SINGLE)
    for tag in settingJsonObj['tagList'].split('>'):
        tagListBox.insert(1, tag)
    addTag = Button(tagFrame, text='Add Tag', command=lambda: addList(tagListBox, 'tagList', 'New Tag', 'Enter Tag(s)'))
    removeTag = Button(tagFrame, text='Remove Tag', command=lambda: removeList_(tagListBox, 'tagList', 'Remove Failed', 'Cannot remove all tags. To download without a tag, use "all" as the tag.'))
    resetTag  = Button(tagFrame, text='Reset Tags', command=lambda: resetList(tagListBox, 'tagList', 'all'))

    download_group.append(booruNameEntry)
    download_group.append(booruValidate)
    download_group.append(tagListBox)
    download_group.append(addTag)
    download_group.append(removeTag)
    download_group.append(resetTag)
    download_group.append(downloadMode)

    Label(tabDrive, text='Image Download Settings').pack(fill='x')
    tagFrame.pack(fill='y', side='left')
    booruFrame.pack(fill='y', side='left')
    otherFrame.pack(fill='both',side='right')
    
    downloadEnabled.pack()
    downloadHostFrame.pack(fill='both')
    tagListBox.pack(fill='x')
    addTag.pack(fill='x')
    removeTag.pack(fill='x')
    resetTag.pack(fill='x')
    Label(booruFrame, text='Booru Name').pack(fill='x')
    booruNameEntry.pack(fill='x')
    booruValidate.pack(fill='x')
    Label(booruFrame, text='Download Mode').pack(fill='x')
    downloadMode.pack(fill='x')
    downloadResourceEnabled.pack(fill='x')
    
    tabMaster.add(tabWallpaper, text='Wallpaper')
    #==========={WALLPAPER TAB ITEMS} ========================#
    rotateCheckbox = Checkbutton(tabWallpaper, text='Rotate Wallpapers', variable=rotateWallpaperVar, 
                                 command=lambda: toggleAssociateSettings(rotateWallpaperVar.get(), wallpaper_group))
    wpList = Listbox(tabWallpaper, selectmode=SINGLE)
    for key in settingJsonObj['wallpaperDat'].keys():
        wpList.insert(1, key)
    addWPButton = Button(tabWallpaper, text='Add/Edit Wallpaper', command=lambda: addWallpaper(wpList))
    remWPButton = Button(tabWallpaper, text='Remove Wallpaper', command=lambda: removeWallpaper(wpList))
    autoImport  = Button(tabWallpaper, text='Auto Import', command=lambda: autoImportWallpapers(wpList))
    varSlider     = Scale(tabWallpaper, orient='horizontal', label='Rotate Variation (sec)', from_=0, 
                          to=(wallpaperDelayVar.get()-1), variable=wpVarianceVar)
    wpDelaySlider = Scale(tabWallpaper, orient='horizontal', label='Rotate Timer (sec)', from_=5, to=300,
                          variable=wallpaperDelayVar, command=lambda val: updateMax(varSlider, int(val)-1))

    wallpaper_group.append(wpList)
    wallpaper_group.append(addWPButton)
    wallpaper_group.append(remWPButton)
    wallpaper_group.append(wpDelaySlider)
    wallpaper_group.append(autoImport)
    wallpaper_group.append(varSlider)

    rotateCheckbox.pack(fill='x')
    wpList.pack(fill='x')
    addWPButton.pack(fill='x')
    remWPButton.pack(fill='x')
    autoImport.pack(fill='x')
    wpDelaySlider.pack(fill='x')
    varSlider.pack(fill='x')
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
    tabInfoExpound.add(tab_wallpaper, text='Wallpaper')
    Label(tab_wallpaper, text=WALLPAPER_TEXT, anchor='nw', wraplength=460).pack()
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
    toggleAssociateSettings(rotateWallpaperVar.get(), wallpaper_group)
    toggleAssociateSettings(timeoutPopupsVar.get(), timeout_group)
    toggleAssociateSettings(mitosisVar.get(), mitosis_cGroup)
    toggleAssociateSettings(not mitosisVar.get(), mitosis_group)
    toggleAssociateSettings_manual(downloadEnabledVar.get(), download_group, 'white', 'gray25')
    
    tabMaster.pack(expand=1, fill='both')
    tabInfoExpound.pack(expand=1, fill='both')
    saveExitButton.pack(fill='x')
    
    
    
    #first time alert popup
    if not settingJsonObj['is_configed'] == 1: 
        messagebox.showinfo('First Config', 'Config has not been run before. All settings are defaulted to frequency of 0 except for popups.\n[This alert will only appear on the first run of config]')
    #version alert, if core web version (0.0.0) is different from the github configdefault, alerts user that update is available
    #   if user is a bugfix patch behind, the _X at the end of the 0.0.0, they will not be alerted
    #   the version will still be red to draw attention to it
    if local_version.split('_')[0] != webv.split('_')[0]:
        messagebox.showwarning('Update Available', 'Core local version and web version are not the same.\nPlease visit the Github and download the newer files.')
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
            resp = confirmBox(parent, 'Current resource folder will be deleted and overwritten. Is this okay?')
            if not resp:
                return False
            shutil.rmtree(PATH + 'resource\\')
        with zipfile.ZipFile(openLocation.name, 'r') as zip:
            zip.extractall(PATH + 'resource\\')
        messagebox.showinfo('Done', 'Resource importing completed.')
    except Exception as e:
        messagebox.showerror('Read Error', 'Failed to import resources from file.\n[' + str(e) + ']')

def confirmBox(parent, message) -> bool:
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
    Label(root, text=message, wraplength=212).pack(fill='x')
    #Label(root).pack()
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
    settingJsonObj['wallpaperDat'] = str(settingJsonObj['wallpaperDat'])
    settingJsonObj['is_configed'] = 1
    #, command=lambda: toggleStartupBat(startLoginVar.get())
    toggleStartupBat(varList[nameList.index('start_on_logon')].get())
    for name in varNames:
        try:
            p = varList[nameList.index(name)].get()
            temp[name] = p if type(p) is int or type(p) is str else (1 if type(p) is bool and p else 0)
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

def validateBooru(name) -> bool:
    return requests.get(BOORU_URL.replace(BOORU_FLAG, name)).status_code == 200

def getLiveVersion():
    try:
        with open(urllib.request.urlretrieve(UPDCHECK_URL)[0], 'r') as liveDCfg:
            return(liveDCfg.read().split('\n')[1].split(',')[0])
    except:
        return 'Could not check version.'

def addList(tkListObj, key, title, text):
    name = simpledialog.askstring(title, text)
    if(name != '' and name != None):
       settingJsonObj[key] = settingJsonObj[key] + '>' + name
       tkListObj.insert(2, name)
    
def removeList(tkListObj, key, title, text):
    index = int(tkListObj.curselection()[0])
    itemName = tkListObj.get(index)
    if index > 0:
        settingJsonObj[key] = settingJsonObj[key].replace('>' + itemName, '')
        tkListObj.delete(tkListObj.curselection())
    else:
        messagebox.showwarning(title, text)

def removeList_(tkListObj, key, title, text):
    index = int(tkListObj.curselection()[0])
    itemName = tkListObj.get(index)
    print(settingJsonObj[key])
    print(itemName)
    print(len(settingJsonObj[key].split('>')))
    if len(settingJsonObj[key].split('>')) > 1:
        if index > 0:
            settingJsonObj[key] = settingJsonObj[key].replace('>' + itemName, '')
        else:
            settingJsonObj[key] = settingJsonObj[key].replace(itemName + '>', '')
        tkListObj.delete(tkListObj.curselection())
    else:
        messagebox.showwarning(title, text)

def resetList(tkListObj, key, default):
    try:
        tkListObj.delete(0,999)
    except Exception as e:
        print(e)
    settingJsonObj[key] = default
    for obj in settingJsonObj[key].split('>'):
        tkListObj.insert(1,obj)

def addWallpaper(tkListObj):
    path_ = filedialog.askopenfile('r', defaultextension ='.png').name
    if(path_ != '' and path_ != None):
        name =  simpledialog.askstring('Wallpaper Name','Wallpaper Label\n(Name displayed in list)')
        if(name != '' and name != None and name != 'default'):
            settingJsonObj['wallpaperDat'][name] = path_
            tkListObj.insert(1, name)

def removeWallpaper(tkListObj):
    index = int(tkListObj.curselection()[0])
    itemName = tkListObj.get(index)
    if index > 0:
        del settingJsonObj['wallpaperDat'][itemName]
        tkListObj.delete(tkListObj.curselection())
    else:
        messagebox.showwarning('Remove Default', 'You cannot remove the default wallpaper.')

def autoImportWallpapers(tkListObj):
    allow_ = confirmBox(tkListObj, 'Current list will be cleared before new list is imported from the /resource folder. Is that okay?')
    if allow_:
        #clear list
        while True:
            try:
                del settingJsonObj['wallpaperDat'][tkListObj.get(1)]
                tkListObj.delete(1)
            except:
                break
        for file in os.listdir(os.path.join(PATH, 'resource')):
            if((file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg')) and file != 'wallpaper.png'):
                name_ = file.split('.')[0]
                tkListObj.insert(1, name_)
                settingJsonObj['wallpaperDat'][name_] = os.path.join(PATH, 'resource', file)

def updateMax(obj, value):
    obj.configure(to=int(value))

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

def refresh():
    os.startfile('config.pyw')
    os.kill(os.getpid(), 9)

def assignJSON(key, var):
    settingJsonObj[key] = var
    with open(PATH + 'config.cfg', 'w') as f:
        f.write(json.dumps(settingJsonObj))
    
def toggleAssociateSettings(ownerState, objList):
    toggleAssociateSettings_manual(ownerState, objList, 'SystemButtonFace', 'gray25')

def toggleAssociateSettings_manual(ownerState, objList, colorOn, colorOff):
    for obj in objList:
        obj.configure(state=('normal' if ownerState else 'disabled'))
        obj.configure(bg=(colorOn if ownerState else colorOff))

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
    var.set(str(key.keysym))
    parent.destroy()

try:
    spawnWindow()
except Exception as e:
    messagebox.showerror('Could not start', 'Could not start config.\n[' + str(e) + ']')
