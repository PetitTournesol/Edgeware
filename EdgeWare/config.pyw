import json
import os
import shutil
import subprocess
import webbrowser
import zipfile
import pathlib
import ast
import urllib.request
import hashlib
import ctypes
import sys
import logging
import time
from tkinter import Tk, ttk, simpledialog, messagebox, filedialog, IntVar, BooleanVar, StringVar, Frame, Checkbutton, Button, Scale, Label, Toplevel, Entry, OptionMenu, Listbox, SINGLE, DISABLED, GROOVE, RAISED

PATH = f'{str(pathlib.Path(__file__).parent.absolute())}\\'
os.chdir(PATH)

#starting logging
if not os.path.exists(os.path.join(PATH, 'logs')):
    os.mkdir(os.path.join(PATH, 'logs'))
logging.basicConfig(filename=os.path.join(PATH, 'logs', time.asctime().replace(' ', '_').replace(':', '-') + '-dbg.txt'), format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.info('Started config logging successfully.')

def pip_install(packageName:str):
    try:
        logging.info(f'attempting to install {packageName}')
        subprocess.call(f'py -m pip install {packageName}')
    except:
        logging.warning(f'failed to install {packageName} using py -m pip, trying raw pip request')
        subprocess.call(f'pip install {packageName}')
        logging.warning(f'{packageName} should be installed, fatal errors will occur if install failed.')

try:
    import requests
except:
    pip_install('requests')
    import requests

try:
    import PIL
    from PIL import Image, ImageTk
except:
    logging.warning('failed to import pillow module')
    pip_install('pillow')
    from PIL import Image, ImageTk


SYS_ARGS = sys.argv.copy()
SYS_ARGS.pop(0)
logging.info(f'args: {SYS_ARGS}')

#text for the about tab
ANNOYANCE_TEXT          = 'The "Annoyance" section consists of the 5 main configurable settings of Edgeware:\nDelay\nPopup Frequency\nWebsite Frequency\nAudio Frequency\nPromptFrequency\n\nEach is fairly self explanatory, but will still be expounded upon in this section. Delay is the forced time delay between each tick of the "clock" for Edgeware. The longer it is, the slower things will happen. Popup frequency is the percent chance that a randomly selected popup will appear on any given tick of the clock, and similarly for the rest, website being the probability of opening a website or video from /resource/vid/, audio for playing a file from /resource/aud/, and prompt for a typing prompt to pop up.\n\nThese values can be set by adjusting the bars, or by clicking the button beneath each respective slider, which will allow you to type in an explicit number instead of searching for it on the scrollbar.\n\nIn order to disable any feature, lower its probability to 0, to ensure that you\'ll be getting as much of any feature as possible, turn it up to 100.\nThe popup setting "Mitosis mode" changes how popups are displayed. Instead of popping up based on the timer, the program create a single popup when it starts. When the submit button on ANY popup is clicked to close it, a number of popups will open up in its place, as given by the "Mitosis Strength" setting.\n\nPopup timeout will result in popups timing out and closing after a certain number of seconds.'
DRIVE_TEXT              = 'The "Drive" portion of Edgeware has three features: fill drive, replace images, and Booru downloader.\n\n"Fill Drive" does exactly what it says: it attempts to fill your hard drive with as much porn from /resource/img/ as possible. It does, however, have some restrictions. It will (should) not place ANY images into folders that start with a "." or have their names listed in the folder name blacklist.\nIt will also ONLY place images into the User folder and its subfolders.\nFill drive has one modifier, which is its own forced delay. Because it runs with between 1 and 8 threads at any given time, when unchecked it can fill your drive VERY quickly. To ensure that you get that nice slow fill, you can adjust the delay between each folder sweep it performs and the max number of threads.\n\n"Replace Images" is more complicated. Its searching is the exact same as fill drive, but instead of throwing images everywhere, it will seek out folders with large numbers of images (more than the threshold value) and when it finds one, it will replace ALL of the images with porn from /resource/img/. REMEMBER THAT IF YOU CARE ABOUT YOUR PHOTOS, AND THEY\'RE IN A FOLDER WITH MORE IMAGES THAN YOUR CHOSEN THRESHOLD VALUE, EITHER BACK THEM UP IN A ZIP OR SOMETHING OR DO. NOT. USE. THIS SETTING. I AM NOT RESPONSIBLE FOR YOUR OWN DECISION TO RUIN YOUR PHOTOS.\n\nBooru downloader allows you to download new items from a Booru of your choice. For the booru name, ONLY the literal name is used, like "censored" or "blacked" instead of the full url. This is not case sensitive. Use the "Validate" button to ensure that downloading will be successful before running. For tagging, if you want to have mutliple tags, they can be combined using "tag1+tag2+tag3" or if you want to add blacklist tags, type your tag and append a "+-blacklist_tag" after the desired tag.'
STARTUP_TEXT            = 'Start on launch does exactly what it says it does and nothing more: it allows Edgeware to start itself whenever you start up and log into your PC.\n\nPlease note that the method used does NOT edit registry or schedule any tasks. The "lazy startup" method was used for both convenience of implementation and convenience of cleaning.\n\nIf you forget to turn off the "start on logon" setting before uninstalling, you will need to manually go to your Startup folder and remove "edgeware.bat".'
WALLPAPER_TEXT          = 'The Wallpaper section allows you to set up rotating wallpapers of your choice from any location, or auto import all images from the /resource/ folder (NOT /resource/img/ folder) to use as wallpapers.\n\nThe rotate timer is the amount of time the program will wait before rotating to another randomly selected wallpaper, and the rotate variation is the amount above or below that set value that can randomly be selected as the actual wait time.'
HIBERNATE_TEXT          = 'The Hibernate feature is an entirely different mode for Edgeware to operate in.\nInstead of constantly shoving popups, lewd websites, audio, and prompts in your face, hibernate starts quiet and waits for a random amount of time between its provided min and max before exploding with a rapid assortment of your chosen payloads. Once it finishes its barrage, it settles back down again for another random amount of time, ready to strike again when the time is right.\n\n\nThis feature is intend to be a much "calmer" way to use Edgeware; instead of explicitly using it to edge yourself or get off, it\'s supposed to lie in wait for you and perform bursts of self-sabotage to keep drawing you back to porn.'
ADVANCED_TEXT           = 'The Advanced section is also something previously only accessible by directly editing the config.cfg file. It offers full and complete customization of all setting values without any limitations outside of variable typing.\n\n\nPlease use this feature with discretion, as any erroneous values will result in a complete deletion and regeneration of the config file from the default, and certain value ranges are likely to result in crashes or unexpected glitches in the program.'
THANK_AND_ABOUT_TEXT    = 'Thank you so much to all the fantastic artists who create and freely distribute the art that allows programs like this to exist, to all the people who helped me work through the various installation problems as we set the software up (especially early on), and honestly thank you to ALL of the people who are happily using Edgeware. \n\nIt truly makes me happy to know that my work is actually being put to good use by people who enjoy it. After all, at the end of the day that\'s really all I\'ve ever really wanted, but figured was beyond reach of a stupid degreeless neet.\nI love you all <3\n\n\n\nIf you like my work, please feel free to help support my neet lifestyle by donating to $PetitTournesol on Cashapp; by no means are you obligated or expected to, but any and all donations are greatly appreciated!'

#all booru consts
BOORU_FLAG = '<BOORU_INSERT>'                                                      #flag to replace w/ booru name
BOORU_URL  = f'https://{BOORU_FLAG}.booru.org/index.php?page=post&s=list&tags='    #basic url
BOORU_VIEW = f'https://{BOORU_FLAG}.booru.org/index.php?page=post&s=view&id='      #post view url
BOORU_PTAG = '&pid='                                                               #page id tag

#url to check online version
UPDCHECK_URL = 'http://raw.githubusercontent.com/PetitTournesol/Edgeware/main/EdgeWare/configDefault.dat'
local_version = '0.0.0_NOCONNECT'

logging.info('opening configDefault')
with open(f'{PATH}configDefault.dat') as r:
    defaultSettingLines = r.readlines()
    varNames = defaultSettingLines[0].split(',')
    varNames[-1] = varNames[-1].replace('\n', '')
    defaultVars = defaultSettingLines[1].split(',')
logging.info(f'done with configDefault\n\tdefault={defaultVars}')

local_version = defaultVars[0]

settings = {}
for var in varNames:
    settings[var] = defaultVars[varNames.index(var)]

defaultSettings = settings.copy()

if not os.path.exists(f'{PATH}config.cfg'):
    logging.warning('no "config.cfg" file found, creating new "config.cfg".')
    with open(f'{PATH}config.cfg', 'w') as f:
        f.write(json.dumps(settings))
    logging.info('created new config file.')

with open(f'{PATH}config.cfg', 'r') as f:
    logging.info('json loading settings')
    try:
        settings = json.loads(f.readline())
    except Exception as e:
        logging.fatal(f'could not load settings.\n\nReason: {e}')
        exit()


#inserts new settings if versions are literally different 
# or if the count of settings between actual and default is different
if settings['version'] != defaultVars[0] or len(settings) != len(defaultSettings):
    logging.warning('version difference/settingJson len mismatch, regenerating new settings with missing keys...')
    tempSettingDict = {}
    for name in varNames:
        try:
            tempSettingDict[name] = settings[name]
        except:
            tempSettingDict[name] = defaultVars[varNames.index(name)]
            logging.info(f'added missing key: {name}')
    tempSettingDict['version'] = defaultVars[0]
    settings = tempSettingDict.copy()
    with open(f'{PATH}config.cfg', 'w') as f:
        f.write(str(tempSettingDict).replace('\'', '"'))
        logging.info('wrote regenerated settings.')

logging.info('converting wallpaper dict string.')
DEFAULT_WALLPAPERDAT = {'default': 'wallpaper.png'}
try:
    if settings['wallpaperDat'] == 'WPAPER_DEF':
        logging.info('default wallpaper dict inserted.')
        settings['wallpaperDat'] = DEFAULT_WALLPAPERDAT
    else:
        #print(settings['wallpaperDat'])
        if type(settings['wallpaperDat']) == dict:
            logging.info('wallpaper object already dict?')
        else:
            settings['wallpaperDat'] = ast.literal_eval(settings['wallpaperDat'].replace('\\', '/'))
            logging.info('evaluated settings wallpaper str to dict.')
except Exception as e:
    settings['wallpaperDat'] = DEFAULT_WALLPAPERDAT
    logging.warning(f'failed to process wallpaper dict.\n\tReason: {e}\nused default wallpaper dict instead.')

pass_ = ''

def show_window():
    global settings, defaultSettings
    webv = getLiveVersion()

    #window things
    root = Tk()
    root.title('Edgeware Config')
    root.geometry('740x675')
    try:
        root.iconbitmap(f'{PATH}default_assets\\config_icon.ico')
        logging.info('set iconbitmap.')
    except:
        logging.warning('failed to set iconbitmap.')
    fail_loop = 0

    #painful control variables ._.
    while(fail_loop < 2):
        try:
            delayVar            = IntVar(root, value=int(settings['delay']))
            popupVar            = IntVar(root, value=int(settings['popupMod']))
            webVar              = IntVar(root, value=int(settings['webMod']))
            audioVar            = IntVar(root, value=int(settings['audioMod']))
            promptVar           = IntVar(root, value=int(settings['promptMod']))
            fillVar             = BooleanVar(root, value=(settings['fill']==1))

            fillDelayVar        = IntVar(root, value=int(settings['fill_delay']))
            replaceVar          = BooleanVar(root, value=(settings['replace'] == 1))
            replaceThreshVar    = IntVar(root, value=int(settings['replaceThresh']))
            startLoginVar       = BooleanVar(root, value=(settings['start_on_logon'] == 1))

            hibernateVar        = BooleanVar(root, value=(settings['hibernateMode']==1))
            hibernateMinVar     = IntVar(root, value=int(settings['hibernateMin']))
            hibernateMaxVar     = IntVar(root, value=(settings['hibernateMax']))
            wakeupActivityVar   = IntVar(root, value=(settings['wakeupActivity']))

            discordVar          = BooleanVar(root, value=(int(settings['showDiscord'])==1))
            startFlairVar       = BooleanVar(root, value=(int(settings['showLoadingFlair'])==1))
            captionVar          = BooleanVar(root, value=(int(settings['showCaptions'])==1))
            panicButtonVar      = StringVar(root, value=settings['panicButton'])
            panicVar            = BooleanVar(root, value=(int(settings['panicDisabled'])==1))

            promptMistakeVar    = IntVar(root, value=int(settings['promptMistakes']))
            mitosisVar          = BooleanVar(root, value=(int(settings['mitosisMode'])==1))
            onlyVidVar          = BooleanVar(root, value=(int(settings['onlyVid'])==1))
            popupWebVar         = BooleanVar(root, value=(int(settings['webPopup'])==1))

            rotateWallpaperVar  = BooleanVar(root, value=(int(settings['rotateWallpaper'])==1))
            wallpaperDelayVar   = IntVar(root, value=int(settings['wallpaperTimer']))
            wpVarianceVar       = IntVar(root, value=int(settings['wallpaperVariance']))

            timeoutPopupsVar    = BooleanVar(root, value=(int(settings['timeoutPopups'])==1))
            popupTimeoutVar     = IntVar(root, value=(int(settings['popupTimeout'])))
            mitosisStrenVar     = IntVar(root, value=(int(settings['mitosisStrength'])))
            booruNameVar        = StringVar(root, value=settings['booruName'])
            
            downloadEnabledVar  = BooleanVar(root, value=(int(settings['downloadEnabled']) == 1))
            downloadModeVar     = StringVar(root, value=settings['downloadMode'])
            useWebResourceVar   = BooleanVar(root, value=(int(settings['useWebResource'])==1))
            fillPathVar         = StringVar(root, value=settings['drivePath'])
            rosVar              = BooleanVar(root, value=(int(settings['runOnSaveQuit'])==1))

            timerVar            = BooleanVar(root, value=(int(settings['timerMode'])==1))
            timerTimeVar        = IntVar(root, value=int(settings['timerSetupTime']))
            lkCorner            = IntVar(root, value=int(settings['lkCorner']))
            popopOpacity        = IntVar(root, value=int(settings['lkScaling']))
            lkToggle            = BooleanVar(root, value=(int(settings['lkToggle'])==1))

            safewordVar         = StringVar(root, value='password')

            videoVolume         = IntVar(root, value=int(settings['videoVolume']))
            vidVar              = IntVar(root, value=int(settings['vidMod']))
            denialMode          = BooleanVar(root, value=(int(settings['denialMode']) == 1))
            denialChance        = IntVar(root, value=int(settings['denialChance']))
            popupSublim         = IntVar(root, value=(int(settings['popupSubliminals']) == 1))

            booruMin            = IntVar(root, value=int(settings['booruMinScore']))
            
            #grouping for sanity's sake later
            in_var_group = [delayVar, popupVar, webVar, audioVar, promptVar, fillVar, 
                            fillDelayVar, replaceVar, replaceThreshVar, startLoginVar, 
                            hibernateVar, hibernateMinVar, hibernateMaxVar, wakeupActivityVar, 
                            discordVar, startFlairVar, captionVar, panicButtonVar, panicVar, 
                            promptMistakeVar, mitosisVar, onlyVidVar, popupWebVar,
                            rotateWallpaperVar, wallpaperDelayVar, wpVarianceVar,
                            timeoutPopupsVar, popupTimeoutVar, mitosisStrenVar, booruNameVar,
                            downloadEnabledVar, downloadModeVar, useWebResourceVar, fillPathVar, rosVar,
                            timerVar, timerTimeVar, lkCorner, popopOpacity, lkToggle,
                            videoVolume, vidVar, denialMode, denialChance, popupSublim,
                            booruMin]

            in_var_names = ['delay', 'popupMod', 'webMod', 'audioMod', 'promptMod', 'fill', 
                            'fill_delay', 'replace', 'replaceThresh', 'start_on_logon', 
                            'hibernateMode', 'hibernateMin', 'hibernateMax', 'wakeupActivity', 
                            'showDiscord', 'showLoadingFlair', 'showCaptions', 'panicButton', 'panicDisabled',
                            'promptMistakes', 'mitosisMode', 'onlyVid', 'webPopup',
                            'rotateWallpaper', 'wallpaperTimer', 'wallpaperVariance',
                            'timeoutPopups', 'popupTimeout', 'mitosisStrength', 'booruName',
                            'downloadEnabled', 'downloadMode', 'useWebResource', 'drivePath', 'runOnSaveQuit',
                            'timerMode', 'timerSetupTime', 'lkCorner', 'lkScaling', 'lkToggle',
                            'videoVolume', 'vidMod', 'denialMode', 'denialChance', 'popupSubliminals',
                            'booruMinScore']
            break
        except Exception as e:
            messagebox.showwarning(
                        'Settings Warning', 
                        f'File "config.cfg" appears corrupted.\nFile will be restored to default.\n[{e}]'
                        )
            logging.warning(f'failed config var loading.\n\tReason: {e}')
            emergencySettings = {}
            for var in varNames:
                emergencySettings[var] = defaultVars[varNames.index(var)]
            with open(f'{PATH}config.cfg', 'w') as f:
                f.write(json.dumps(emergencySettings))
            with open(f'{PATH}config.cfg', 'r') as f:
                settings = json.loads(f.readline())
            fail_loop += 1

    hasWebResourceVar = BooleanVar(root, os.path.exists(os.path.join(PATH, 'resource', 'webResource.json')))

    #done painful control variables
    
    if getPresets() is None:
        write_save(in_var_group, in_var_names, '', False)
        savePreset('Default')

    #grouping for enable/disable
    hibernate_group = []
    fill_group      = []
    replace_group   = []
    mitosis_group   = []
    mitosis_cGroup  = []
    wallpaper_group = []
    timeout_group   = []
    download_group  = []
    timer_group     = []
    lowkey_group    = []
    denial_group    = []

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

    Label(tabGeneral, text='Hibernate Settings', font='Default 13', relief=GROOVE).pack(pady=2)
    hibernateHostFrame.pack(fill='x')
    hibernateFrame.pack(fill='y', side='left')
    toggleHibernateButton.pack(fill='x', side='left', expand=1)
    hibernateMinFrame.pack(fill='y', side='left')
    hibernateMinScale.pack(fill='y')
    hibernateMinButton.pack(fill='y')
    hibernateMaxScale.pack(fill='y')
    hibernateMaxButton.pack(fill='y')
    hibernateMaxFrame.pack(fill='x', side='left')
    h_activityScale.pack(fill='y', side='left')

    #timer settings
    Label(tabGeneral, text='Timer Settings', font='Default 13', relief=GROOVE).pack(pady=2)
    timerFrame = Frame(tabGeneral, borderwidth=5, relief=RAISED)
    
    timerToggle = Checkbutton(timerFrame, text='Timer Mode', variable=timerVar, command=lambda: toggleAssociateSettings(timerVar.get(), timer_group))
    timerSlider = Scale(timerFrame, label='Timer Time (mins)', from_=1, to=1440, orient='horizontal', variable=timerTimeVar)
    safewordFrame = Frame(timerFrame)

    Label(safewordFrame, text='Emergency Safeword').pack()
    timerSafeword = Entry(safewordFrame, show='*', textvariable=safewordVar)
    timerSafeword.pack(expand=1, fill='both')

    timer_group.append(timerSafeword)
    timer_group.append(timerSlider)

    timerToggle.pack(side='left', fill='x', padx=5)
    timerSlider.pack(side='left', fill='x', expand=1, padx=10)
    safewordFrame.pack(side='right', fill='x', padx=5)

    timerFrame.pack(fill='x')

    #mode preset section
    Label(tabGeneral, text='Mode Presets', font='Default 13', relief=GROOVE).pack(pady=2)
    presetFrame = Frame(tabGeneral, borderwidth=5, relief=RAISED)
    dropdownSelectFrame = Frame(presetFrame)

    style_list = [_.split('.')[0].capitalize() for _ in getPresets() if _.endswith('.cfg')]
    logging.info(f'pulled style_list={style_list}')
    styleStr = StringVar(root, style_list.pop(0))

    styleDropDown = OptionMenu(dropdownSelectFrame, styleStr, styleStr.get(), 
                                *style_list, command=lambda key: changeDescriptText(key))
    def changeDescriptText(key:str):
        descriptNameLabel.configure(text=f'{key} Description')
        descriptLabel.configure(text=getDescriptText(key))

    def updateHelperFunc(key:str):
        styleStr.set(key)
        changeDescriptText(key)

    def doSave() -> bool:
        name_ = simpledialog.askstring('Save Preset', 'Preset name')
        existed = os.path.exists(os.path.join(PATH, 'presets', f'{name_.lower()}.cfg'))
        if name_ != None and name != '':
            write_save(in_var_group, in_var_names, safewordVar, False)
            if existed:
                if messagebox.askquestion('Overwrite', 'A preset with this name already exists. Overwrite it?') == 'no':
                    return False
        if savePreset(name_) and not existed:
            style_list.insert(0, 'Default')
            style_list.append(name_.capitalize())
            styleStr.set('Default')
            styleDropDown['menu'].delete(0, 'end')
            for item in style_list:
                styleDropDown['menu'].add_command(label=item, command=lambda x=item: updateHelperFunc(x))
            styleStr.set(style_list[0])
        return True

    confirmStyleButton = Button(dropdownSelectFrame, text='Load Preset', command=lambda: applyPreset(styleStr.get()))
    saveStyleButton = Button(dropdownSelectFrame, text='Save Preset', command=doSave)

    presetDescriptFrame = Frame(presetFrame, borderwidth=2, relief=GROOVE)

    descriptNameLabel = Label(presetDescriptFrame, text='Default Description', font='Default 15')
    descriptLabel = Label(presetDescriptFrame, text='Default Text Here', relief=GROOVE, wraplength=580)
    changeDescriptText('Default')

    dropdownSelectFrame.pack(side='left', fill='x', padx=6)
    styleDropDown.pack(fill='x', expand=1)
    confirmStyleButton.pack(fill='both', expand=1)
    Label(dropdownSelectFrame).pack(fill='both', expand=1)
    Label(dropdownSelectFrame).pack(fill='both', expand=1)
    saveStyleButton.pack(fill='both', expand=1)

    presetDescriptFrame.pack(side='right', fill='both', expand=1)
    descriptNameLabel.pack(fill='y', pady=4)
    descriptLabel.pack(fill='both', expand=1)

    presetFrame.pack(fill='both', expand=1)

    #other
    Label(tabGeneral, text='Other', font='Default 13', relief=GROOVE).pack(pady=2)
    otherHostFrame = Frame(tabGeneral, borderwidth=5, relief=RAISED)
    resourceFrame = Frame(otherHostFrame)
    exportResourcesButton = Button(resourceFrame, text='Export resource', command=exportResource)
    importResourcesButton = Button(resourceFrame, text='Import resources', command=lambda: importResource(root))
    toggleFrame1 = Frame(otherHostFrame)
    toggleFrame2 = Frame(otherHostFrame)

    toggleStartupButton = Checkbutton(toggleFrame1, text='Launch on Startup', variable=startLoginVar)
    toggleDiscordButton = Checkbutton(toggleFrame1, text='Show on Discord', variable=discordVar)
    toggleFlairButton = Checkbutton(toggleFrame2, text='Show Loading Flair', variable=startFlairVar)
    toggleROSButton = Checkbutton(toggleFrame2, text='Run Edgeware on Save & Exit', variable=rosVar)

    otherHostFrame.pack(fill='x')
    resourceFrame.pack(fill='y', side='left')
    exportResourcesButton.pack(fill='x')
    importResourcesButton.pack(fill='x')
    toggleFrame1.pack(fill='both', side='left', expand=1)
    toggleStartupButton.pack(fill='x')
    toggleDiscordButton.pack(fill='x')
    toggleFrame2.pack(fill='both', side='left', expand=1)
    toggleFlairButton.pack(fill='x')
    toggleROSButton.pack(fill='x')

    Label(tabGeneral, text='Information', font='Default 13', relief=GROOVE).pack(pady=2)
    infoHostFrame = Frame(tabGeneral, borderwidth=5, relief=RAISED)
    zipGitFrame = Frame(infoHostFrame)
    verFrame = Frame(infoHostFrame)
    #zipDropdown = OptionMenu(tabGeneral, zipDropVar, *DOWNLOAD_STRINGS)
    #zipDownloadButton = Button(tabGeneral, text='Download Zip', command=lambda: downloadZip(zipDropVar.get(), zipLabel))
    zipLabel = Label(zipGitFrame, text=f'Current Zip:\n{pickZip()}', background='lightgray', wraplength=100)
    local_verLabel = Label(verFrame, text=f'Local Version:\n{defaultVars[0]}')
    web_verLabel = Label(verFrame, text=f'GitHub Version:\n{webv}', bg=('SystemButtonFace' if (defaultVars[0] == webv) else 'red'))
    openGitButton = Button(zipGitFrame, text='Open Github', command=lambda: webbrowser.open('https://github.com/PetitTournesol/Edgeware'))

    infoHostFrame.pack(fill='x')
    zipGitFrame.pack(fill='both', side='left', expand=1)
    zipLabel.pack(fill='x')
    openGitButton.pack(fill='both', expand=1)
    verFrame.pack(fill='both', side='left', expand=1)
    local_verLabel.pack(fill='x')
    web_verLabel.pack(fill='x')

    forceReload = Button(infoHostFrame, text='Force Reload', command=refresh)
    optButton   = Button(infoHostFrame, text='Test Func', command=lambda: getDescriptText('default'))

    saveExitButton = Button(root, text='Save & Exit', command=lambda: write_save(in_var_group, in_var_names, safewordVar, True))

    #force reload button for debugging, only appears on DEV versions
    if local_version.endswith('DEV'):
        forceReload.pack(fill='y', expand=1)
        optButton.pack(fill='y', expand=1)
    
    #zipDownloadButton.grid(column=0, row=10) #not using for now until can find consistent direct download
    #zipDropdown.grid(column=0, row=9)
    #==========={HERE ENDS  GENERAL TAB ITEM INITS}===========#
    tabMaster.add(tabAnnoyance, text='Annoyance')

    Label(tabAnnoyance).pack()

    delayModeFrame = Frame(tabAnnoyance, borderwidth=5, relief=RAISED)
    delayFrame = Frame(delayModeFrame)
    lowkeyFrame = Frame(delayModeFrame)

    delayScale = Scale(delayFrame, label='Timer Delay (ms)', from_=10, to=60000, orient='horizontal', variable=delayVar)
    delayManual = Button(delayFrame, text='Manual delay...', command=lambda: assign(delayVar, simpledialog.askinteger('Manual Delay', prompt='[10-60000]: ')))
    opacityScale = Scale(tabAnnoyance, label='Popup Opacity (%)', from_=5, to=100, orient='horizontal', variable=popopOpacity)

    posList = ['Top Right', 'Top Left', 'Bottom Left', 'Bottom Right', 'Random']
    lkItemVar = StringVar(root, posList[lkCorner.get()])
    lowkeyDropdown = OptionMenu(lowkeyFrame, lkItemVar, *posList, command=lambda x: (lkCorner.set(posList.index(x))))
    lowkeyToggle = Checkbutton(lowkeyFrame, text='Lowkey Mode', variable=lkToggle, command=lambda: toggleAssociateSettings(lkToggle.get(), lowkey_group))

    lowkey_group.append(lowkeyDropdown)
    
    delayModeFrame.pack(fill='x')

    delayScale.pack(fill='x', expand=1)
    delayManual.pack(fill='x', expand=1)
    
    delayFrame.pack(side='left', fill='x', expand=1)

    lowkeyFrame.pack(fill='y', side='left')
    lowkeyDropdown.pack(fill='x', padx=2, pady = 5)
    lowkeyToggle.pack(fill='both', expand=1)

    opacityScale.pack(fill='x')
    
    #popup frame handling
    popupHostFrame = Frame(tabAnnoyance, borderwidth=5, relief=RAISED)
    popupFrame = Frame(popupHostFrame)
    timeoutFrame = Frame(popupHostFrame)
    mitosisFrame = Frame(popupHostFrame)
    panicFrame = Frame(popupHostFrame)
    denialFrame = Frame(popupHostFrame)
    
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

    setPanicButtonButton = Button(panicFrame, text=f'Set Panic Button\n<{panicButtonVar.get()}>', command=lambda:getKeyboardInput(setPanicButtonButton, panicButtonVar))
    doPanicButton = Button(panicFrame, text='Perform Panic', command=lambda: os.startfile('panic.pyw'))
    panicDisableButton = Checkbutton(popupHostFrame, text='Disable Panic Hotkey', variable=panicVar)

    popupWebToggle= Checkbutton(popupHostFrame, text='Popup close opens web page', variable=popupWebVar)
    toggleCaptionsButton = Checkbutton(popupHostFrame, text='Popup Captions', variable=captionVar)
    toggleSubliminalButton = Checkbutton(popupHostFrame, text='Popup Subliminals', variable=popupSublim)

    timeoutToggle = Checkbutton(timeoutFrame, text='Popup Timeout', variable=timeoutPopupsVar, command=lambda: toggleAssociateSettings(timeoutPopupsVar.get(), timeout_group))
    timeoutSlider = Scale(timeoutFrame, label='Time (sec)', from_=1, to=120, orient='horizontal', variable=popupTimeoutVar)

    timeout_group.append(timeoutSlider)

    denialSlider = Scale(denialFrame, label='Denial Chance', orient='horizontal', variable=denialChance)
    denialToggle = Checkbutton(denialFrame, text='Denial Mode', variable=denialMode, command=lambda: toggleAssociateSettings(denialMode.get(), denial_group))

    denial_group.append(denialSlider)

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
    denialFrame.pack(fill='y', side='left')
    denialSlider.pack(fill='x')
    denialToggle.pack(fill='x')
    panicFrame.pack(fill='y', side='left')
    setPanicButtonButton.pack(fill='x')
    doPanicButton.pack(fill='x')
    panicDisableButton.pack(fill='x')
    popupWebToggle.pack(fill='x')
    toggleCaptionsButton.pack(fill='x')
    toggleSubliminalButton.pack(fill='x')
    #popup frame handle end

    #other start
    otherHostFrame = Frame(tabAnnoyance, borderwidth=5, relief=RAISED)

    audioFrame = Frame(otherHostFrame)
    webFrame = Frame(otherHostFrame)
    vidFrameL = Frame(otherHostFrame)
    vidFrameR = Frame(otherHostFrame)
    promptFrame = Frame(otherHostFrame)
    mistakeFrame = Frame(otherHostFrame)

    audioScale = Scale(audioFrame, label='Audio Freq (%)', from_=0, to=100, orient='horizontal', variable=audioVar)
    audioManual = Button(audioFrame, text='Manual audio...', command=lambda: assign(audioVar, simpledialog.askinteger('Manual Audio', prompt='[0-100]: ')))
    
    webScale = Scale(webFrame, label='Website Freq (%)', from_=0, to=100, orient='horizontal', variable=webVar)
    webManual = Button(webFrame, text='Manual web...', command=lambda: assign(webVar, simpledialog.askinteger('Web Chance', prompt='[0-100]: ')))
    
    vidScale = Scale(vidFrameL, label='Video Chance (%)', from_=0, to=100, orient='horizontal', variable=vidVar)
    vidManual = Button(vidFrameL, text='Manual vid...', command=lambda: assign(vidVar, simpledialog.askinteger('Video Chance', prompt='[0-100]: ')))
    vidVolumeScale = Scale(vidFrameR, label='Video Volume', from_=0, to=100, orient='horizontal', variable=videoVolume)
    vidVolumeManual = Button(vidFrameR, text='Manual volume...', command=lambda: assign(videoVolume, simpledialog.askinteger('Video Volume', prompt='[0-100]: ')))
    
    promptScale = Scale(promptFrame, label='Prompt Freq (%)', from_=0, to=100, orient='horizontal', variable=promptVar)
    promptManual = Button(promptFrame, text='Manual prompt...', command=lambda: assign(promptVar, simpledialog.askinteger('Manual Prompt', prompt='[0-100]: ')))

    mistakeScale = Scale(mistakeFrame, label='Prompt Mistakes', from_=0, to=150, orient='horizontal', variable=promptMistakeVar)
    mistakeManual = Button(mistakeFrame, text='Manual mistakes...', command=lambda: assign(promptMistakeVar, simpledialog.askinteger('Max Mistakes', prompt='Max mistakes allowed in prompt text\n[0-150]: ')))
    
    otherHostFrame.pack(fill='x')

    audioScale.pack(fill='x', padx=3, expand=1)
    audioManual.pack(fill='x')
    audioFrame.pack(side='left')

    webFrame.pack(fill='y', side='left', padx=3, expand=1)
    webScale.pack(fill='x')
    webManual.pack(fill='x')

    vidFrameL.pack(fill='x', side='left', padx=(3, 0), expand=1)
    vidScale.pack(fill='x')
    vidManual.pack(fill='x')
    vidFrameR.pack(fill='x', side='left', padx=(0, 3), expand=1)
    vidVolumeScale.pack(fill='x')
    vidVolumeManual.pack(fill='x')
    
    promptFrame.pack(fill='y', side='left', padx=(3,0), expand=1)
    promptScale.pack(fill='x')
    promptManual.pack(fill='x')
    mistakeFrame.pack(fill='y', side='left', padx=(0, 3), expand=1)
    mistakeScale.pack(fill='x')
    mistakeManual.pack(fill='x')
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
        if path_ != '':
            settings['drivePath'] = path_
            pathBox.configure(state='normal')
            pathBox.delete(0, 9999)
            pathBox.insert(1, path_)
            pathBox.configure(state='disabled')
            fillPathVar.set(str(pathBox.get()))
    pathBox = Entry(pathFrame)
    pathButton = Button(pathFrame, text='Select', command=local_assignPath)

    pathBox.insert(1, settings['drivePath'])
    pathBox.configure(state='disabled')

    fillBox = Checkbutton(fillFrame, text='Fill Drive', variable=fillVar, command=lambda: toggleAssociateSettings(fillVar.get(), fill_group))
    fillDelay = Scale(fillFrame, label='Fill Delay (10ms)', from_=0, to=250, orient='horizontal', variable=fillDelayVar)
    
    fill_group.append(fillDelay)
    
    replaceBox = Checkbutton(fillFrame, text='Replace Images', variable=replaceVar, command=lambda: toggleAssociateSettings(replaceVar.get(), replace_group))
    replaceThreshScale = Scale(fillFrame, label='Image Threshold', from_=1, to=1000, orient='horizontal', variable=replaceThreshVar)
    
    replace_group.append(replaceThreshScale)

    avoidHostFrame = Frame(hardDriveFrame)

    avoidListBox = Listbox(avoidHostFrame, selectmode=SINGLE)
    for name in settings['avoidList'].split('>'):
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
    minScoreSlider = Scale(booruFrame, from_=-50, to=100, orient='horizontal', variable=booruMin, label='Minimum Score')
    
    booruValidate  = Button(booruFrame, text='Validate', command=lambda: (
        messagebox.showinfo('Success!', 'Booru is valid.') 
        if validateBooru(booruNameVar.get()) else 
        messagebox.showerror('Failed', 'Booru is invalid.')
    ))

    tagListBox = Listbox(tagFrame, selectmode=SINGLE)
    for tag in settings['tagList'].split('>'):
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
    download_group.append(minScoreSlider)

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
    minScoreSlider.pack(fill='x')
    downloadResourceEnabled.pack(fill='x')
    
    tabMaster.add(tabWallpaper, text='Wallpaper')
    #==========={WALLPAPER TAB ITEMS} ========================#
    rotateCheckbox = Checkbutton(tabWallpaper, text='Rotate Wallpapers', variable=rotateWallpaperVar, 
                                 command=lambda: toggleAssociateSettings(rotateWallpaperVar.get(), wallpaper_group))
    wpList = Listbox(tabWallpaper, selectmode=SINGLE)
    for key in settings['wallpaperDat']:
        wpList.insert(1, key)
    addWPButton = Button(tabWallpaper, text='Add/Edit Wallpaper', command=lambda: addWallpaper(wpList))
    remWPButton = Button(tabWallpaper, text='Remove Wallpaper', command=lambda: removeWallpaper(wpList))
    autoImport  = Button(tabWallpaper, text='Auto Import', command=lambda: autoImportWallpapers(wpList))
    varSlider     = Scale(tabWallpaper, orient='horizontal', label='Rotate Variation (sec)', from_=0, 
                          to=(wallpaperDelayVar.get()-1), variable=wpVarianceVar)
    wpDelaySlider = Scale(tabWallpaper, orient='horizontal', label='Rotate Timer (sec)', from_=5, to=300,
                          variable=wallpaperDelayVar, command=lambda val: updateMax(varSlider, int(val)-1))
    
    pHoldImageR = Image.open(os.path.join(PATH, 'default_assets', 'default_win10.jpg')).resize((int(root.winfo_screenwidth()*0.13), int(root.winfo_screenheight()*0.13)), Image.NEAREST)
    
    def updatePanicPaper():
        nonlocal pHoldImageR
        selectedFile = filedialog.askopenfile('rb', filetypes=[
            ('image file', '.jpg .jpeg .png')
        ])
        if not isinstance(selectedFile, type(None)):
            try:
                img = Image.open(selectedFile.name).convert('RGB')
                img.save(os.path.join(PATH, 'default_assets', 'default_win10.jpg'))
                pHoldImageR = ImageTk.PhotoImage(img.resize((int(root.winfo_screenwidth()*0.13), int(root.winfo_screenheight()*0.13)), Image.NEAREST))
                panicWallpaperLabel.config(image=pHoldImageR)
                panicWallpaperLabel.update_idletasks()
            except Exception as e:
                logging.warning(f'failed to open/change default wallpaper\n{e}')

    panicWPFrame = Frame(tabWallpaper)
    panicWPFrameL = Frame(panicWPFrame)
    panicWPFrameR = Frame(panicWPFrame)
    panicWallpaperImage = ImageTk.PhotoImage(pHoldImageR)
    panicWallpaperButton = Button(panicWPFrameL, text='Change Panic Wallpaper', command=updatePanicPaper)
    panicWallpaperLabel = Label(panicWPFrameR, text='Current Panic Wallpaper', image=panicWallpaperImage)

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
    panicWPFrame.pack(fill='x', expand=1)
    panicWPFrameL.pack(side='left', fill='y')
    panicWPFrameR.pack(side='right', fill='x', expand=1)
    panicWallpaperButton.pack(fill='x', padx=5, pady=5, expand=1)
    Label(panicWPFrameR, text='Current Panic Wallpaper').pack(fill='x')
    panicWallpaperLabel.pack()
    tabMaster.add(tabAdvanced, text='Advanced')
    #==========={IN HERE IS ADVANCED TAB ITEM INITS}===========#
    itemList = []
    for settingName in settings:
        itemList.append(settingName)
    dropdownObj = StringVar(root, itemList[0])
    textObj = StringVar(root, settings[dropdownObj.get()])
    advPanel = Frame(tabAdvanced)
    textInput = Entry(advPanel)
    textInput.insert(1, textObj.get())
    expectedLabel = Label(tabAdvanced, text=f'Expected value: {defaultSettings[dropdownObj.get()]}')
    dropdownMenu = OptionMenu(advPanel, dropdownObj, *itemList, command=lambda a: updateText([textInput, expectedLabel], settings[a], a))
    dropdownMenu.configure(width=10)
    applyButton = Button(advPanel, text='Apply', command= lambda: assignJSON(dropdownObj.get(), textInput.get()))
    Label(tabAdvanced).pack()
    Label(tabAdvanced, text='Be careful messing with some of these; improper configuring can cause\nproblems when running, or potentially cause unintended damage to files.').pack()
    Label(tabAdvanced).pack()
    Label(tabAdvanced).pack()
    advPanel.pack(fill='x', padx=2)
    dropdownMenu.pack(padx=2, side='left')
    textInput.pack(padx=2, fill='x', expand=1, side='left')
    applyButton.pack(padx=2, fill='x', side='right')
    expectedLabel.pack()
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
    toggleAssociateSettings(timerVar.get(), timer_group)
    toggleAssociateSettings(lkToggle.get(), lowkey_group)
    toggleAssociateSettings(denialMode.get(), denial_group)
    
    tabMaster.pack(expand=1, fill='both')
    tabInfoExpound.pack(expand=1, fill='both')
    saveExitButton.pack(fill='x')
    
    
    timeObjPath = os.path.join(PATH, 'hid_time.dat')
    HIDDEN_ATTR = 0x02
    SHOWN_ATTR  = 0x08
    ctypes.windll.kernel32.SetFileAttributesW(timeObjPath, SHOWN_ATTR)
    if os.path.exists(timeObjPath):
        with open(timeObjPath, 'r') as file:
            time_ = int(file.readline()) / 60
            if not time_ == int(settings['timerSetupTime']):
                timerToggle.configure(state=DISABLED)
                for item in timer_group:
                    item.configure(state=DISABLED)
    ctypes.windll.kernel32.SetFileAttributesW(timeObjPath, HIDDEN_ATTR)

    
    #first time alert popup
    #if not settings['is_configed'] == 1: 
    #    messagebox.showinfo('First Config', 'Config has not been run before. All settings are defaulted to frequency of 0 except for popups.\n[This alert will only appear on the first run of config]')
    #version alert, if core web version (0.0.0) is different from the github configdefault, alerts user that update is available
    #   if user is a bugfix patch behind, the _X at the end of the 0.0.0, they will not be alerted
    #   the version will still be red to draw attention to it
    if local_version.split('_')[0] != webv.split('_')[0] and not local_version.endswith('DEV'):
        messagebox.showwarning('Update Available', 'Core local version and web version are not the same.\nPlease visit the Github and download the newer files.')
    root.mainloop()

def pickZip() -> str:
    #selecting zip
    for dirListObject in os.listdir(f'{PATH}\\'):
        try:
            if dirListObject.split('.')[-1].lower() == 'zip':
                return dirListObject.split('.')[0]
        except:
            print('{} is not a zip file.'.format(dirListObject))
    return '[No Zip Found]'

def exportResource() -> bool:
    try:
        logging.info('starting zip export...')
        saveLocation = filedialog.asksaveasfile('w', defaultextension ='.zip')
        with zipfile.ZipFile(saveLocation.name, 'w', compression=zipfile.ZIP_DEFLATED) as zip:
            beyondRoot = False
            for root, dirs, files in os.walk(os.path.join(PATH, 'resource')):
                for file in files:
                    logging.info(f'write {file}')
                    if beyondRoot:
                        zip.write(os.path.join(root, file), root.split('\\')[-1] + f'\\{file}')
                    else:
                        zip.write(os.path.join(root, file), f'\\{file}')
                for dir in dirs:
                    logging.info(f'make dir {dir}')
                    zip.write(os.path.join(root, dir), f'\\{dir}\\')
                beyondRoot = True
        return True
    except Exception as e:
        logging.fatal(f'failed to export zip\n\tReason: {e}')
        messagebox.showerror('Write Error', 'Failed to export resource to zip file.')
        return False

def importResource(parent:Tk) -> bool:
    try:
        openLocation = filedialog.askopenfile('r', defaultextension ='.zip')
        if openLocation == None:
            return False
        if os.path.exists(f'{PATH}resource\\'):
            resp = confirmBox(parent, 'Current resource folder will be deleted and overwritten. Is this okay?')
            if not resp:
                logging.info('exited import resource overwrite')
                return False
            shutil.rmtree(f'{PATH}resource\\')
            logging.info('removed old resource folder')
        with zipfile.ZipFile(openLocation.name, 'r') as zip:
            zip.extractall(f'{PATH}resource\\')
            logging.info('extracted all from zip')
        messagebox.showinfo('Done', 'Resource importing completed.')
        return True
    except Exception as e:
        messagebox.showerror('Read Error', f'Failed to import resources from file.\n[{e}]')
        return False

def confirmBox(parent:Tk, message:str) -> bool:
    allow = False
    root = Toplevel(parent)
    def complete(state:bool) -> bool:
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

def write_save(varList:list[StringVar | IntVar | BooleanVar], nameList:list[str], passVar:str, exitAtEnd:bool):
    logging.info('starting config save write...')
    temp = json.loads('{}')
    settings['wallpaperDat'] = str(settings['wallpaperDat'])
    settings['wallpaperDat'] = f'{settings["wallpaperDat"]}'
    settings['is_configed'] = 1

    toggleStartupBat(varList[nameList.index('start_on_logon')].get())

    SHOWN_ATTR = 0x08
    HIDDEN_ATTR = 0x02
    hashObjPath = os.path.join(PATH, 'pass.hash')
    timeObjPath = os.path.join(PATH, 'hid_time.dat')

    if int(varList[nameList.index('timerMode')].get()) == 1:
        toggleStartupBat(True)

        #revealing hidden files
        ctypes.windll.kernel32.SetFileAttributesW(hashObjPath, SHOWN_ATTR)
        ctypes.windll.kernel32.SetFileAttributesW(timeObjPath, SHOWN_ATTR)
        logging.info('revealed hashed pass and time files')

        with open(hashObjPath, 'w') as passFile, open(timeObjPath, 'w') as timeFile:
            logging.info('attempting file writes...')
            passFile.write(hashlib.sha256(passVar.get().encode(encoding='ascii',errors='ignore')).hexdigest())
            timeFile.write(str(varList[nameList.index('timerSetupTime')].get()*60))
            logging.info('wrote files.')

        #hiding hash file with saved password hash for panic and time data
        ctypes.windll.kernel32.SetFileAttributesW(hashObjPath, HIDDEN_ATTR)
        ctypes.windll.kernel32.SetFileAttributesW(timeObjPath, HIDDEN_ATTR)
        logging.info('hid hashed pass and time files')
    else:
        try:
            if not varList[nameList.index('start_on_logon')].get():
                toggleStartupBat(False)
            ctypes.windll.kernel32.SetFileAttributesW(hashObjPath, SHOWN_ATTR)
            ctypes.windll.kernel32.SetFileAttributesW(timeObjPath, SHOWN_ATTR)
            os.remove(hashObjPath)
            os.remove(timeObjPath)
            logging.info('removed pass/time files.')
        except Exception as e:
            errText = str(e).lower().replace(os.environ['USERPROFILE'].lower().replace('\\', '\\\\'), '[USERNAME_REDACTED]')
            logging.warning(f'failed timer file modifying\n\tReason: {errText}')
            pass

    for name in varNames:
        try:
            p = varList[nameList.index(name)].get()
            #standard named variables
            temp[name] = p if type(p) is int or type(p) is str else (1 if type(p) is bool and p else 0)
        except:
            #nonstandard named variables
            try:
                temp[name] = int(settings[name])
            except:
                temp[name] = settings[name]

    with open(f'{PATH}config.cfg', 'w') as file:
        file.write(json.dumps(temp))
        logging.info(f'wrote config file: {json.dumps(temp)}')

    if int(varList[nameList.index('runOnSaveQuit')].get()) == 1 and exitAtEnd:
        os.startfile('start.pyw')

    if exitAtEnd:
        logging.info('exiting config')
        os.kill(os.getpid(), 9)

def validateBooru(name:str) -> bool:
    return requests.get(BOORU_URL.replace(BOORU_FLAG, name)).status_code == 200

def getLiveVersion() -> str:
    try:
        logging.info('fetching github version')
        with open(urllib.request.urlretrieve(UPDCHECK_URL)[0], 'r') as liveDCfg:
            return(liveDCfg.read().split('\n')[1].split(',')[0])
    except Exception as e:
        logging.warning('failed to fetch github version.\n\tReason: {e}')
        return 'Could not check version.'

def addList(tkListObj:Listbox, key:str, title:str, text:str):
    name = simpledialog.askstring(title, text)
    if name != '' and name != None:
       settings[key] = f'{settings[key]}>{name}'
       tkListObj.insert(2, name)
    
def removeList(tkListObj:Listbox, key:str, title:str, text:str):
    index = int(tkListObj.curselection()[0])
    itemName = tkListObj.get(index)
    if index > 0:
        settings[key] = settings[key].replace(f'>{itemName}', '')
        tkListObj.delete(tkListObj.curselection())
    else:
        messagebox.showwarning(title, text)

def removeList_(tkListObj:Listbox, key:str, title:str, text:str):
    index = int(tkListObj.curselection()[0])
    itemName = tkListObj.get(index)
    print(settings[key])
    print(itemName)
    print(len(settings[key].split('>')))
    if len(settings[key].split('>')) > 1:
        if index > 0:
            settings[key] = settings[key].replace(f'>{itemName}', '')
        else:
            settings[key] = settings[key].replace(f'{itemName}>', '')
        tkListObj.delete(tkListObj.curselection())
    else:
        messagebox.showwarning(title, text)

def resetList(tkListObj:Listbox, key:str, default):
    try:
        tkListObj.delete(0,999)
    except Exception as e:
        print(e)
    settings[key] = default
    for setting in settings[key].split('>'):
        tkListObj.insert(1,setting)

def addWallpaper(tkListObj:Listbox):
    file = filedialog.askopenfile('r', filetypes=[
        ('image file', '.jpg .jpeg .png')
    ])
    if not isinstance(file, type(None)):
        lname =  simpledialog.askstring('Wallpaper Name','Wallpaper Label\n(Name displayed in list)')
        if not isinstance(lname, type(None)):
            print(file.name.split('/')[-1])
            settings['wallpaperDat'][lname] = file.name.split('/')[-1]
            tkListObj.insert(1, lname)

def removeWallpaper(tkListObj):
    index = int(tkListObj.curselection()[0])
    itemName = tkListObj.get(index)
    if index > 0:
        del settings['wallpaperDat'][itemName]
        tkListObj.delete(tkListObj.curselection())
    else:
        messagebox.showwarning('Remove Default', 'You cannot remove the default wallpaper.')

def autoImportWallpapers(tkListObj:Listbox):
    allow_ = confirmBox(tkListObj, 'Current list will be cleared before new list is imported from the /resource folder. Is that okay?')
    if allow_:
        #clear list
        while True:
            try:
                del settings['wallpaperDat'][tkListObj.get(1)]
                tkListObj.delete(1)
            except:
                break
        for file in os.listdir(os.path.join(PATH, 'resource')):
            if (file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg')) and file != 'wallpaper.png':
                name_ = file.split('.')[0]
                tkListObj.insert(1, name_)
                settings['wallpaperDat'][name_] = file

def updateMax(obj, value:int):
    obj.configure(to=int(value))

def updateText(objList:Entry or Label, var:str, var_Label:str):
    try:
        for obj in objList:
            if isinstance(obj, Entry):
                obj.delete(0, 9999)
                obj.insert(1, var)
            elif isinstance(obj, Label):
                obj.configure(text=f'Expected value: {defaultSettings[var_Label]}')
    except:
        print('idk what would cause this but just in case uwu')

def refresh():
    os.startfile('config.pyw')
    os.kill(os.getpid(), 9)

def assignJSON(key:str, var:int or str):
    settings[key] = var
    with open(f'{PATH}config.cfg', 'w') as f:
        f.write(json.dumps(settings))
    
def toggleAssociateSettings(ownerState:bool, objList:list):
    toggleAssociateSettings_manual(ownerState, objList, 'SystemButtonFace', 'gray25')

def toggleAssociateSettings_manual(ownerState:bool, objList:list, colorOn:int, colorOff:int):
    logging.info(f'toggling state of {objList} to {ownerState}')
    for tkObject in objList:
        tkObject.configure(state=('normal' if ownerState else 'disabled'))
        tkObject.configure(bg=(colorOn if ownerState else colorOff))

def shortcut_script(pth_str:str, startup_path:str, title:str):
    #strings for batch script to write vbs script to create shortcut on desktop
    #stupid and confusing? yes. the only way i could find to do this? also yes.
    print(pth_str)
    return ['@echo off\n'
            'set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"\n',
            'echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%\n',
            f'echo sLinkFile = "{startup_path}\\{title}.lnk" >> %SCRIPT%\n',
            'echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%\n',
            f'echo oLink.WorkingDirectory = "{pth_str}\\" >> %SCRIPT%\n',
            f'echo oLink.TargetPath = "{pth_str}\\start.pyw" >> %SCRIPT%\n',
            'echo oLink.Save >> %SCRIPT%\n',
            'cscript /nologo %SCRIPT%\n',
            'del %SCRIPT%']

#uses the above script to create a shortcut on desktop with given specs
def make_shortcut(tList:list) -> bool:
    with open(PATH + '\\tmp.bat', 'w') as bat:
        bat.writelines(shortcut_script(tList[0], tList[1], tList[2])) #write built shortcut script text to temporary batch file
    try:
        logging.info(f'making shortcut to {tList[2]}')
        subprocess.call(PATH + '\\tmp.bat')
        os.remove(PATH + '\\tmp.bat')
        return True
    except Exception as e:
        print('failed')
        logging.warning(f'failed to call or remove temp batch file for making shortcuts\n\tReason: {e}')
        return False

def toggleStartupBat(state:bool):
    try:
        startup_path = os.path.expanduser('~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\')
        logging.info(f'trying to toggle startup bat to {state}')
        if state:
            make_shortcut([PATH, startup_path, 'edgeware']) #i scream at my previous and current incompetence and poor programming
            logging.info('toggled startup run on.')
        else:
            os.remove(os.path.join(startup_path, 'edgeware.lnk'))
            logging.info('toggled startup run off.')
    except Exception as e:
        errText = str(e).lower().replace(os.environ['USERPROFILE'].lower().replace('\\', '\\\\'), '[USERNAME_REDACTED]')
        logging.warning(f'failed to toggle startup bat.\n\tReason: {errText}')
        print('uwu')

def assign(obj:StringVar or IntVar or BooleanVar, var:str or int or bool):
    try:
        obj.set(var)
    except:
        ''
        #no assignment

def getKeyboardInput(button:Button, var:StringVar):
    child = Tk()
    child.resizable(False,False)
    child.title('Key Listener')
    child.wm_attributes('-topmost', 1)
    child.geometry('250x250')
    child.focus_force()
    Label(child, text='Press any key or exit').pack(expand=1, fill='both')
    child.bind('<KeyPress>', lambda key: assignKey(child, button, var, key))
    child.mainloop()

def assignKey(parent:Tk, button:Button, var:StringVar, key):
    button.configure(text=f'Set Panic Button\n<{key.keysym}>')
    var.set(str(key.keysym))
    parent.destroy()


def getPresets() -> list[str]:
    presetFolderPath = os.path.join(PATH, 'presets')
    if not os.path.exists(presetFolderPath):
        os.mkdir(presetFolderPath)
    return os.listdir(presetFolderPath) if len(os.listdir(presetFolderPath)) > 0 else None

def applyPreset(name:str):
    try:
        os.remove(os.path.join(PATH, 'config.cfg'))
        shutil.copyfile(os.path.join(PATH, 'presets', f'{name}.cfg'), os.path.join(PATH, 'config.cfg'))
        refresh()
    except Exception as e:
        messagebox.showerror('Error', 'Failed to load preset.\n\n{e}')

def savePreset(name:str) -> bool:
    try:
        if name is not None and name != '':
            shutil.copyfile(os.path.join(PATH, 'config.cfg'), os.path.join(PATH, 'presets', f'{name.lower()}.cfg'))
            with open(os.path.join(PATH, 'presets', f'{name.lower()}.cfg'), 'rw') as file:
                file_json = json.loads(file.readline())
                file_json['drivePath'] = 'C:/Users/'
                file.write(json.dumps(file_json))
            return True
        return False
    except:
        return True

def getDescriptText(name:str) -> str:
    try:
        with open(os.path.join(PATH, 'presets', f'{name}.txt'), 'r') as file:
            text = ''
            for line in file.readlines():
                text += line
            return text
    except:
        return 'This preset has no description file.'

if __name__ == '__main__':
    try:
        show_window()
    except Exception as e:
        logging.fatal(f'Config encountered fatal error:\n{e}')
        messagebox.showerror('Could not start', f'Could not start config.\n[{e}]')
