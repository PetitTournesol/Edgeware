import urllib
import pathlib
import ctypes
import hashlib
import os
import subprocess
import ast
import time
import webbrowser
import zipfile
import shutil
import json
import random as rand
import threading as thread
import tkinter as tk
import logging
import sys
from PIL import Image
from dataclasses import dataclass
from tkinter import messagebox, simpledialog

PATH = str(pathlib.Path(__file__).parent.absolute())
os.chdir(PATH)

#starting logging
if not os.path.exists(os.path.join(PATH, 'logs')):
    os.mkdir(os.path.join(PATH, 'logs'))
logging.basicConfig(filename=os.path.join(PATH, 'logs', time.asctime().replace(' ', '_').replace(':', '-') + '-ew_start.txt'), format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.info('Started start logging successfully.')

SYS_ARGS = sys.argv.copy()
SYS_ARGS.pop(0)
logging.info(f'args: {SYS_ARGS}')

settings = {}
#func for loading settings, really just grouping it
def load_settings():
    global settings
    logging.info('loading config settings...')
    settings = {}

    #creating objects to check vs live config for version updates
    with open(PATH + '\\configDefault.dat') as r:
        logging.info('reading in default config values')
        defaultLines = r.readlines()
        default_setting_keys = defaultLines[0].split(',')
        default_setting_keys[-1] = default_setting_keys[-1].replace('\n', '')
        default_setting_values = defaultLines[1].split(',')

    for var in default_setting_keys:
        settings[var] = default_setting_values[default_setting_keys.index(var)]

    #checking if config file exists and then writing the default config settings to a new file if it doesn't
    if not os.path.exists(f'{PATH}\\config.cfg'):
        with open(f'{PATH}\\config.cfg', 'w') as f:
            f.write(json.dumps(settings))
            logging.warning('could not find config.cfg, wrote new file.')

    #reading in config file
    with open(f'{PATH}\\config.cfg', 'r') as f:
        settings = json.loads(f.readline())
        logging.info('read in settings from config.cfg')

    #if the config version and the version listed in the configdefault version are different to try to update with
    #new setting tags if any are missing.
    if settings['version'] != default_setting_values[0]:
        logging.warning(f'local version {settings["version"]} does not match default version, config will be updated')
        regen_settings = {}
        for obj in default_setting_keys:
            try:
                regen_settings[obj] = settings[obj]
            except:
                logging.info(f'added missing key: {obj}')
                regen_settings[obj] = default_setting_values[default_setting_keys.index(obj)]
        regen_settings['version'] = default_setting_values[0]
        regen_settings = json.loads(str(regen_settings).replace('\'', '"'))
        settings = regen_settings
        with open(f'{PATH}\\config.cfg', 'w') as f:
            f.write(str(regen_settings).replace('\'', '"'))
            logging.info('wrote updated config to config.cfg')

    #handling proper initialization of wallpapers
    default_wallpaper_dict = {'default': 'wallpaper.png'}
    logging.info('converting wallpaper string to dict')
    try:
        if settings['wallpaperDat'] == 'WPAPER_DEF':
            logging.info('default wallpaper data used')
            settings['wallpaperDat'] = default_wallpaper_dict
        else:
            print(settings['wallpaperDat'])
            if type(settings['wallpaperDat']) == dict:
                logging.info('wallpaperdat already dict')
                print('passed')
            else:
                settings['wallpaperDat'] = ast.literal_eval(settings['wallpaperDat'].replace('\\', '/'))
                logging.info('parsed wallpaper dict from string')
    except Exception as e:
        settings['wallpaperDat'] = default_wallpaper_dict
        logging.warning(f'failed to parse wallpaper from string, using default value instead\n\tReason: {e}')

#load settings, if first run open options, then reload options from file
load_settings()
if not settings['is_configed']==1:
    logging.info('running config for first setup, is_configed flag is false.')
    subprocess.call('pythonw config.pyw')
    logging.info('reloading settings')
    load_settings()

#check for pip_installed flag, if not installed run get-pip.pyw and then install pillow for popups
if not int(settings['pip_installed'])==1:
    logging.warning('pip is not installed, running get-pip.pyw')
    subprocess.call('python get-pip.pyw')
    logging.warning('pip should be installed, but issues will occur if installation failed.')
    settings['pip_installed'] = 1
    with open(f'{PATH}\\config.cfg', 'w') as f:
        f.write(json.dumps(settings))

def pip_install(packageName:str):
    try:
        logging.info(f'attempting to install {packageName}')
        subprocess.call(f'py -m pip install {packageName}')
    except:
        logging.warning(f'failed to install {packageName} using py -m pip, trying raw pip request')
        subprocess.call(f'pip install {packageName}')
        logging.warning(f'{packageName} should be installed, fatal errors will occur if install failed.')

#i liked the emergency fix so much that i just made it import every non-standard lib like that c:
try:
    import requests
except:
    logging.warning('failed to import requests module')
    pip_install('requests')
    import requests

try:
    import PIL
except:
    logging.warning('failed to import pillow module')
    pip_install('pillow')

try:
    import pypresence
except:
    logging.warning('failed to import pypresence module')
    pip_install('pypresence')

try:
    import pystray
except:
    logging.warning('failed to import pystray module')
    pip_install('pystray')

try:
    import playsound
except:
    logging.warning('failed to import playsound module')
    pip_install('playsound==1.2.2')
    import playsound

try:
    import videoprops
except:
    logging.warning('failed to import videoprops module')
    pip_install('get-video-properties')

try:
    import imageio
except:
    logging.warning('failed to import imageio module')
    pip_install('imageio')

try:
    import moviepy
except:
    logging.warning('failed to import moviepy module')
    pip_install('moviepy')

try:
    import sounddevice
except:
    logging.warning('failed to import moviepy module')
    pip_install('sounddevice')

try:
    from bs4 import BeautifulSoup
except:
    logging.warning('failed to import bs4 module')
    pip_install('bs4')
    from bs4 import BeautifulSoup

#end non-standard imports

DESKTOP_PATH = os.path.join(os.environ['USERPROFILE'], 'Desktop') #desktop path for making shortcuts
AVOID_LIST = ['EdgeWare', 'AppData'] #default avoid list for fill/replace
FILE_TYPES = ['png', 'jpg', 'jpeg'] #recognized file types for replace
RESOURCE_PATHS = ['\\resource\\', '\\resource\\aud\\', '\\resource\\img\\', '\\resource\\vid\\']

LIVE_FILL_THREADS = 0 #count of live threads for hard drive filling
PLAYING_AUDIO = False #audio thread flag
REPLACING_LIVE = False #replace thread flag
HAS_PROMPTS = False #can use prompts flag
MITOSIS_LIVE = False #flag for if the mitosis mode popup has been spawned

#default data for generating working default asset resource folder
DEFAULT_WEB = '{"urls":["https://duckduckgo.com/"], "args":["?q=why+are+you+gay"]}'
DEFAULT_PROMPT = '{"moods":["no moods"], "freqList":[100], "minLen":1, "maxLen":1, "no moods":["no prompts"]}'
DEFAULT_DISCORD = 'Playing with myself~'

#naming each used variable from config for ease of use later
#annoyance vars
DELAY = int(settings['delay'])
POPUP_CHANCE = int(settings['popupMod'])
AUDIO_CHANCE = int(settings['audioMod'])
PROMPT_CHANCE = int(settings['promptMod'])
VIDEO_CHANCE = int(settings['vidMod'])
WEB_CHANCE = int(settings['webMod'])

VIDEOS_ONLY = int(settings['onlyVid']) == 1

PANIC_DISABLED = int(settings['panicDisabled']) == 1

#mode vars
SHOW_ON_DISCORD = int(settings['showDiscord']) == 1
LOADING_FLAIR = int(settings['showLoadingFlair'])==1

DOWNLOAD_ENABLED = int(settings['downloadEnabled']) == 1
USE_WEB_RESOURCE = int(settings['useWebResource']) == 1

MAX_FILL_THREADS = int(settings['maxFillThreads'])

HIBERNATE_MODE = int(settings['hibernateMode']) == 1
HIBERNATE_MIN = int(settings['hibernateMin'])
HIBERNATE_MAX = int(settings['hibernateMax'])
WAKEUP_ACTIVITY = int(settings['wakeupActivity'])

FILL_MODE = int(settings['fill']) == 1
FILL_DELAY = int(settings['fill_delay'])
REPLACE_MODE = int(settings['replace']) == 1
REPLACE_THRESHOLD = int(settings['replaceThresh'])

ROTATE_WALLPAPER = int(settings['rotateWallpaper']) == 1

MITOSIS_MODE = int(settings['mitosisMode']) == 1
LOWKEY_MODE = int(settings['lkToggle']) == 1

TIMER_MODE = int(settings['timerMode']) == 1

DRIVE_PATH = settings['drivePath']

def shortcut_script(pth_str:str, keyword:str, script:str, title:str):
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
def make_shortcut(tList:list) -> bool:
    with open(PATH + '\\tmp.bat', 'w') as bat:
        bat.writelines(tList) #write built shortcut script text to temporary batch file
    try:
        logging.info(f'making shortcut to {tList[2]}')
        subprocess.call(PATH + '\\tmp.bat')
        os.remove(PATH + '\\tmp.bat')
        return True
    except Exception as e:
        print('failed')
        logging.warning(f'failed to call or remove temp batch file for making shortcuts\n\tReason: {e}')
        return False

#for checking directories/files
def file_exists(dir:str) -> bool:
    return os.path.exists(PATH + dir)
#same as file_exists but checking paths on the desktop specifically
def desktop_file_exists(obj:str) -> bool:
    return os.path.exists(os.path.join(DESKTOP_PATH, obj))

#start init portion, check resources, config, etc.
try:
    if not file_exists('\\resource\\'):
        logging.warning('no resource folder found')
        pth = 'pth-default_ignore'
        #selecting first zip found in script folder
        for obj in os.listdir(PATH + '\\'):
            try:
                if obj.split('.')[-1].lower() == 'zip':
                    logging.info(f'found zip file {obj}')
                    pth = f'{PATH}\\{obj}'
                    break
            except:
                print(f'{obj} is not a zip file.')
        #if found zip unpack
        if not pth == 'pth-default_ignore':
           with zipfile.ZipFile(pth, 'r') as obj:
                logging.info('extracting resources from zip')
                obj.extractall(PATH + '\\resource\\')
        else:
            #if no zip found, use default resources
            logging.warning('no zip file found, generating resource folder from default assets.')
            for obj in RESOURCE_PATHS:
                os.mkdir(PATH + obj)
            default_path = PATH + '\\default_assets\\'
            output_path = PATH + '\\resource\\'
            shutil.copyfile(f'{default_path}default_wallpaper.png', f'{output_path}wallpaper.png')
            shutil.copyfile(f'{default_path}default_image.png', f'{output_path}img\\img0.png', follow_symlinks=True)
            if not os.path.exists(f'{output_path}discord.dat'):
                with open(f'{output_path}discord.dat', 'w') as f:
                    f.write(DEFAULT_DISCORD)
            if not os.path.exists(f'{output_path}prompt.json'):
                with open(f'{output_path}prompt.json', 'w') as f:
                    f.write(DEFAULT_PROMPT)
            if not os.path.exists(f'{output_path}web.json'):
                with open(f'{output_path}web.json', 'w') as f:
                    f.write(DEFAULT_WEB)
except Exception as e:
    messagebox.showerror('Launch Error', 'Could not launch Edgeware due to resource zip unpacking issues.\n[' + str(e) + ']')
    logging.fatal(f'failed to unpack resource zip or read default resources.\n\tReason:{e}')
    os.kill(os.getpid(), 9)

HAS_PROMPTS = False
WEB_JSON_FOUND = False
if os.path.exists(PATH + '\\resource\\prompt.json'):
    logging.info('found prompt.json')
    HAS_PROMPTS = True
if os.path.exists(PATH + '\\resource\\web.json'):
    logging.info('found web.json')
    WEB_JSON_FOUND = True

WEB_DICT = {}
if os.path.exists(PATH + '\\resource\\web.json'):
    with open(PATH + '\\resource\\web.json', 'r') as webF:
        WEB_DICT = json.loads(webF.read())

try:
    AVOID_LIST = settings['avoidList'].split('>')
except Exception as e:
    logging.warning(f'failed to set avoid list\n\tReason: {e}')

#checking presence of resources
try:
    HAS_IMAGES = len(os.listdir(PATH + '\\resource\\img\\')) > 0
    logging.info('image resources found')
except Exception as e:
    logging.warning(f'no image resource folder found\n\tReason: {e}')
    print('no image folder found')
    HAS_IMAGES = False

VIDEOS = []
try:
    for vid in os.listdir(PATH + '\\resource\\vid\\'):
        VIDEOS.append(PATH + '\\resource\\vid\\' + vid)
    logging.info('video resources found')
except Exception as e:
    logging.warning(f'no video resource folder found\n\tReason: {e}')
    print('no video folder found')

AUDIO = []
try:
    for aud in os.listdir(PATH + '\\resource\\aud\\'):
        AUDIO.append(PATH + '\\resource\\aud\\' + aud)
    logging.info('audio resources found')
except:
    logging.warning(f'no audio resource folder found\n\tReason: {e}')
    print('no audio folder found')

HAS_WEB = WEB_JSON_FOUND and len(WEB_DICT['urls']) > 0
#end of checking resource presence

#set discord status if enabled
if SHOW_ON_DISCORD:
    try:
        os.startfile('disc_handler.pyw')
    except Exception as e:
        logging.warning(f'failed to start discord status background task\n\tReason: {e}')
        print('failed to start discord status')

#making missing desktop shortcuts
if not desktop_file_exists('Edgeware.lnk'):
    make_shortcut(shortcut_script(PATH, 'default', 'start.pyw', 'Edgeware'))
if not desktop_file_exists('Config.lnk'):
    make_shortcut(shortcut_script(PATH, 'config', 'config.pyw', 'Config'))
if not desktop_file_exists('Panic.lnk'):
    make_shortcut(shortcut_script(PATH, 'panic', 'panic.pyw', 'Panic'))

if LOADING_FLAIR:
    logging.info('started loading flair')
    subprocess.call('pythonw startup_flair.pyw')

#set wallpaper
if not HIBERNATE_MODE:
    logging.info('set user wallpaper to default wallpaper.png')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, PATH + '\\resource\\wallpaper.png', 0)

#selects url to be opened in new tab by web browser
def url_select(arg:int):
    logging.info(f'selected url {arg}')
    return WEB_DICT['urls'][arg] + WEB_DICT['args'][arg].split(',')[rand.randrange(len(WEB_DICT['args'][arg].split(',')))]

#class to handle window for tray icon
class TrayHandler:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Edgeware')
        self.timer_mode = settings['timerMode'] == 1
        
        self.option_list = [pystray.MenuItem('Edgeware Menu', print), pystray.MenuItem('Panic', self.try_panic)]
        self.tray_icon = pystray.Icon('Edgeware',
                                    Image.open(os.path.join(PATH, 'default_assets', 'default_icon.ico')),
                                    'Edgeware',
                                    self.option_list)

        self.root.withdraw()

        self.password_setup()

    def password_setup(self):
        if self.timer_mode:
            hashObjPath = os.path.join(PATH, 'pass.hash')
            try:
                HIDDEN_ATTR = 0x02
                SHOWN_ATTR = 0x08
                ctypes.windll.kernel32.SetFileAttributesW(hashObjPath, SHOWN_ATTR)
                with open(hashObjPath, 'r') as file:
                    self.hashedPass = file.readline()
                ctypes.windll.kernel32.SetFileAttributesW(hashObjPath, HIDDEN_ATTR)
            except:
                #no hash found
                self.hashedPass = None

    def try_panic(self):
        logging.info('attempting tray panic')
        if not PANIC_DISABLED:
            if self.timer_mode:
                hashObjPath = os.path.join(PATH, 'pass.hash')
                timeObjPath = os.path.join(PATH, 'hid_time.dat')
                pass_ = simpledialog.askstring('Panic', 'Enter Panic Password')
                t_hash = None if pass_ is None or pass_ == '' else hashlib.sha256(pass_.encode(encoding='ascii', errors='ignore')).hexdigest()
                if t_hash == self.hashedPass:
                    #revealing hidden files
                    try:
                        SHOWN_ATTR = 0x08
                        ctypes.windll.kernel32.SetFileAttributesW(hashObjPath, SHOWN_ATTR)
                        ctypes.windll.kernel32.SetFileAttributesW(timeObjPath, SHOWN_ATTR)
                        os.remove(hashObjPath)
                        os.remove(timeObjPath)
                        os.startfile('panic.pyw')
                    except:
                        logging.critical('panic initiated due to failed pass/timer check')
                        self.tray_icon.stop()
                        os.startfile('panic.pyw')
            else:
                logging.warning('panic initiated from tray command')
                self.tray_icon.stop()
                os.startfile('panic.pyw')

    def move_to_tray(self):
        self.tray_icon.run(tray_setup)
        logging.info('tray handler thread running')

def tray_setup(icon):
    icon.visible = True

#main function, probably can do more with this but oh well i'm an idiot so
def main():
    logging.info('entered main function')
    #set up tray icon
    tray = TrayHandler()

    #if tray icon breaks again this is why
    #idk why it works 50% of the time when it works and sometimes just stops working
    thread.Thread(target=tray.move_to_tray, daemon=True).start()

    #timer handling, start if there's a time left file
    if os.path.exists(os.path.join(PATH, 'hid_time.dat')):
        thread.Thread(target=do_timer).start()
    
    #do downloading for booru stuff
    if settings.get('downloadEnabled') == 1:
        booru_downloader:BooruDownloader = BooruDownloader(settings.get('booruName'), settings.get('tagList').split('>'))

        logging.info('start booru_method thread')
        if settings.get('downloadMode') == 'First Page':
            thread.Thread(target=lambda: booru_downloader.download(min_score=int(settings.get('booruMinScore'))), daemon=True).start()
        elif settings.get('downloadMode') == 'Random Page':
            thread.Thread(target=lambda: booru_downloader.download_random(min_score=int(settings.get('booruMinScore'))), daemon=True).start()
        else:
            thread.Thread(target=lambda: booru_downloader.download_all(min_score=int(settings.get('booruMinScore'))), daemon=True).start()

    #do downloading from web resource folder
    if USE_WEB_RESOURCE:
        logging.info('start download_web_resources thread')
        thread.Thread(target=download_web_resources).start()

    #start thread for wallpaper timer
    if ROTATE_WALLPAPER:
        logging.info('start rotate_wallpapers thread')
        thread.Thread(target=rotate_wallpapers).start()

    #run annoyance thread or do hibernate mode
    if HIBERNATE_MODE:
        logging.info('starting in hibernate mode')
        while True:
            waitTime = rand.randint(HIBERNATE_MIN, HIBERNATE_MAX)
            time.sleep(float(waitTime))
            ctypes.windll.user32.SystemParametersInfoW(20, 0, PATH + '\\resource\\wallpaper.png', 0)
            for i in range(0, rand.randint(int(WAKEUP_ACTIVITY / 2), WAKEUP_ACTIVITY)):
                roll_for_initiative()
    else:
        logging.info('starting annoyance loop')
        annoyance()

#just checking %chance of doing annoyance options
def do_roll(mod:int) -> bool:
    return mod > rand.randint(0, 100)

#booru handling class
class BooruDownloader:
    def __init__(self, booru:str, tags:list[str]=None):
        
        self.extension_list:list[str] = ['jpg', 'jpeg', 'png', 'gif']

        self.exception_list:dict[str, BooruScheme] = {
            'rule34':BooruScheme('rule34', 
                                 'https://www.rule34.xxx/index.php?page=post&s=list&tags=', 
                                 '/thumbnails/', 
                                 '/', 
                                 'thumbnail_', 
                                 '.', 
                                 'score:', 
                                 ' ', 
                                 'https://us.rule34.xxx//images/{code_actual}/')
        }

        self.booru          = booru
        self.tags           = '+'.join(tags) if tags is not None else 'all'
        logging.info(f'tags={self.tags}')
        self.post_per_page  = 0
        self.page_count     = 0
        self.booru_scheme   = BooruScheme(self.booru) if self.booru not in self.exception_list.keys() else self.exception_list.get(self.booru)
        self.max_page       = int(self.get_page_count())

    def download(self, page_start:int = 0, page_end:int = 1, min_score:int = None) -> None:
        self._page_start = max(page_start, 0)
        self._page_start = min(self._page_start, self.page_count)
        self._page_end   = min(page_end, self.max_page+1) if page_end >= self._page_start else self._page_start + 1

        for page_index in range(self._page_start, self._page_end):
            self._page_url = f'{self.booru_scheme.booru_search_url.format(booru_name=self.booru)}{self.tags}&pid={page_index*self.post_per_page}'
            logging.info(f'downloadpageurl={self._page_url}')
            self._html = requests.get(self._page_url).text
            self._soup = BeautifulSoup(self._html, 'html.parser')

            for image in self._soup.find_all('img'):
                try:
                    self._src:str     = image.get('src')
                    self._code_actual = int(self.pick_value(self._src, 
                                                       f'{self.booru_scheme.preview_thumb_id_start}', 
                                                       f'{self.booru_scheme.preview_thumb_id_end}'))
                    self._file_name   = self.pick_value(self._src, 
                                                   f'{self.booru_scheme.preview_thumb_name_start}', 
                                                   f'{self.booru_scheme.preview_thumb_name_end}')
                    
                    self._title:str = image.get('title')
                    self._start     = int(self._title.index(f'{self.booru_scheme.score_start}') + len(self.booru_scheme.score_start))
                    self._end       = self._title.index(f'{self.booru_scheme.score_end}', self._start)
                    self._score     = int(self._title[self._start:self._end])

                    if min_score is not None and self._score < min_score:
                        print(f'(score {self._score} too low) skipped {self._src}')
                        continue
                except Exception as e:
                    print(f'skipped: {e}')
                    continue

                for extension in self.extension_list:
                    try:
                        self._file_name_full = f'{self._file_name}.{extension}'
                        self._full_url = f'{self.booru_scheme.raw_image_url.format(booru=self.booru, code_actual=self._code_actual)}{self._file_name_full}'
                        self.direct_download(self._full_url)
                        break
                    except:
                        continue
    
    def download_random(self, min_score:int=None) -> None:
        self._selected_page = rand.randint(0, self.max_page)
        self.download(self._selected_page, min_score=min_score)

    def download_all(self, min_score:int=None) -> None:
        for page in range(0, self.max_page):
            self.download(page, min_score=min_score)

    def direct_download(self, url:str) -> None:
        class LocalOpener(urllib.request.FancyURLopener):
            version = 'Mozilla/5.0'
        with LocalOpener().open(url) as file, open(os.path.join(PATH, 'resource', 'img', url.split('/')[-1]), 'wb') as out:
            logging.info(f'downloaded {url}')
            shutil.copyfileobj(file, out)

    def get_page_count(self) -> int:
        self._href_core = self.booru_scheme.booru_search_url.format(booru_name=self.booru).split('?')[0]
        print(f'href_core={self._href_core}')
        self._home_url  = f'{self._href_core}?page=post&s=list&tags={self.tags}'
        print(self._home_url)
        self._html = requests.get(self._home_url).text
        self._soup = BeautifulSoup(self._html, 'html.parser')
        for a in self._soup.find_all('a'):
            if a.getText() == '2' and self.post_per_page == 0:
                self.post_per_page = int(a.get('href').split('=')[-1])
            if a.get('alt') == 'last page':
                self._final_link = f'{self._href_core}{a.get("href")}'
                print(f'last alt={self._final_link}')
                return (int(self._final_link[(self._final_link.index('&pid=') + len('&pid=')):]) / self.post_per_page + 1)
        return 0

    def pick_value(self, text:str, start_text:str, end_text:str) -> str:
        start_index = text.index(start_text) + len(start_text)
        end_index   = text.index(end_text, start_index)
        return text[start_index:end_index]

@dataclass
class BooruScheme:
    booru_name               : str
    booru_search_url         : str = 'https://{booru_name}.booru.org/index.php?page=post&s=list&tags='
    preview_thumb_id_start   : str = 'thumbnails//'
    preview_thumb_id_end     : str = '/'
    preview_thumb_name_start : str = 'thumbnail_'
    preview_thumb_name_end   : str = '.'
    score_start              : str = 'score:'
    score_end                : str = ' '
    raw_image_url            : str = 'https://img.booru.org/{booru}//images/{code_actual}/' 

#downloads all images listed in webresource.json in resources
def download_web_resources():
    try:
        with open(os.path.join(PATH, 'resource', 'webResource.json')) as op:
            js = json.loads(op.read())
            ls = js['weblist']
            for link in ls:
                BooruDownloader.direct_download(link)
    except Exception as e:
        print(e)

#does annoyance things; while running, does a check of randint against the frequency of each option
#   if pass, do thing, if fail, don't do thing. pretty simple stuff right here.
#   only exception is for fill drive and replace images:
#       fill: will only happen if fill is on AND until there are 8 threads running simultaneously
#             as threads become available they will be restarted.
#       replace: will only happen one single time in the run of the application, but checks ALL folders
def annoyance():
    global MITOSIS_LIVE
    while(True):
        roll_for_initiative()
        if not MITOSIS_LIVE and (MITOSIS_MODE or LOWKEY_MODE) and HAS_IMAGES:
            os.startfile('popup.pyw')
            MITOSIS_LIVE = True
        if FILL_MODE and LIVE_FILL_THREADS < MAX_FILL_THREADS:
            thread.Thread(target=fill_drive).start()
        if REPLACE_MODE and not REPLACING_LIVE:
            thread.Thread(target=replace_images).start()
        time.sleep(float(DELAY) / 1000.0)

#independently attempt to do all active settings with probability equal to their freq value     
def roll_for_initiative():
    if do_roll(WEB_CHANCE) and HAS_WEB:
        try:
            url = url_select(rand.randrange(len(WEB_DICT['urls']))) if HAS_WEB else None
            webbrowser.open_new(url)
        except Exception as e:
            messagebox.showerror('Web Error', 'Failed to open website.\n[' + str(e) + ']')
            logging.critical(f'failed to open website {url}\n\tReason: {e}')
    if do_roll(VIDEO_CHANCE) and VIDEOS:
        try:
            thread.Thread(target=lambda: subprocess.call('pyw popup.pyw -video', shell=False)).start()
        except Exception as e:
            messagebox.showerror('Popup Error', 'Failed to start popup.\n[' + str(e) + ']')
            logging.critical(f'failed to start video popup.pyw\n\tReason: {e}')
    
    if (not (MITOSIS_MODE or LOWKEY_MODE)) and do_roll(POPUP_CHANCE) and HAS_IMAGES:
        try:
            os.startfile('popup.pyw')
        except Exception as e:
            messagebox.showerror('Popup Error', 'Failed to start popup.\n[' + str(e) + ']')
            logging.critical(f'failed to start popup.pyw\n\tReason: {e}')
    if do_roll(AUDIO_CHANCE) and not PLAYING_AUDIO and AUDIO:
        try:
            thread.Thread(target=play_audio).start()
        except:
            messagebox.showerror('Audio Error', 'Failed to play audio.\n[' + str(e) + ']')
            logging.critical(f'failed to play audio\n\tReason: {e}')
    if do_roll(PROMPT_CHANCE) and HAS_PROMPTS:
        try:
            subprocess.call('pythonw prompt.pyw')
        except:
            messagebox.showerror('Prompt Error', 'Could not start prompt.\n[' + str(e) + ']')
            logging.critical(f'failed to start prompt.pyw\n\tReason: {e}')

def rotate_wallpapers():
    prv = 'default'
    base = int(settings['wallpaperTimer'])
    vari = int(settings['wallpaperVariance'])
    while len(settings['wallpaperDat'].keys()) > 1:
        time.sleep(base + rand.randint(-vari, vari))
        selectedWallpaper = list(settings['wallpaperDat'].keys())[rand.randrange(0, len(settings['wallpaperDat'].keys()))]
        while(selectedWallpaper == prv):
            selectedWallpaper = list(settings['wallpaperDat'].keys())[rand.randrange(0, len(settings['wallpaperDat'].keys()))]
        ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(PATH, 'resource', settings['wallpaperDat'][selectedWallpaper]), 0)
        prv = selectedWallpaper

def do_timer():
    hashObjPath = os.path.join(PATH, 'pass.hash')
    timeObjPath = os.path.join(PATH, 'hid_time.dat')

    HIDDEN_ATTR = 0x02
    SHOWN_ATTR  = 0x08
    ctypes.windll.kernel32.SetFileAttributesW(timeObjPath, SHOWN_ATTR)
    with open(timeObjPath, 'r') as file:
        time_remaining = int(file.readline())
    
    while time_remaining > 0:
        print('time left: ', str(time_remaining), 'secs', sep='')
        time.sleep(1)
        time_remaining -= 1
        ctypes.windll.kernel32.SetFileAttributesW(timeObjPath, SHOWN_ATTR)
        with open(timeObjPath, 'w') as file:
            file.write(str(time_remaining))
        ctypes.windll.kernel32.SetFileAttributesW(timeObjPath, HIDDEN_ATTR)

    try:
        ctypes.windll.kernel32.SetFileAttributesW(hashObjPath, SHOWN_ATTR)
        ctypes.windll.kernel32.SetFileAttributesW(timeObjPath, SHOWN_ATTR)
        os.remove(hashObjPath)
        os.remove(timeObjPath)
        os.startfile('panic.pyw')
    except:
        os.startfile('panic.pyw')


#if audio is not playing, selects and plays random audio file from /aud/ folder
def play_audio():
    global PLAYING_AUDIO
    if not AUDIO:
        return
    logging.info('starting audio playback')
    PLAYING_AUDIO = True
    #winsound.PlaySound(AUDIO[rand.randrange(len(AUDIO))], winsound.SND_FILENAME)
    playsound.playsound(AUDIO[rand.randrange(len(AUDIO))])
    PLAYING_AUDIO = False
    logging.info('finished audio playback')

#fills drive with copies of images from /resource/img/
#   only targets User folders; none of that annoying elsaware shit where it fills folders you'll never see
#   can only have 8 threads live at once to avoid 'memory leak'
def fill_drive():
    global LIVE_FILL_THREADS
    LIVE_FILL_THREADS += 1
    docPath = DRIVE_PATH.replace('/', '\\') + '\\'#os.path.expanduser('~\\')
    images = []
    imageNames = []
    logging.info(f'starting drive fill to {docPath}')
    for img in os.listdir(PATH + '\\resource\\img\\'):
        if not img.split('.')[-1] == 'ini':
            images.append(open(os.path.join(PATH, 'resource\\img', img), 'rb').read())
            imageNames.append(img)
    for root, dirs, files in os.walk(docPath):
        #tossing out directories that should be avoided
        for obj in list(dirs):
            if obj in AVOID_LIST or obj[0] == '.':
                dirs.remove(obj)
        for i in range(rand.randint(3, 6)):
            index = rand.randint(0, len(images)-1)
            tObj = str(time.time() * rand.randint(10000, 69420)).encode(encoding='ascii',errors='ignore')
            pth = os.path.join(root, hashlib.md5(tObj).hexdigest() + '.' + str.split(imageNames[index], '.')[len(str.split(imageNames[index], '.')) - 1].lower())
            shutil.copyfile(os.path.join(PATH, 'resource\\img', imageNames[index]), pth)
        time.sleep(float(FILL_DELAY) / 100)
    LIVE_FILL_THREADS -= 1

#seeks out folders with a number of images above the replace threshold and replaces all images with /resource/img/ files 
def replace_images():
    global REPLACING_LIVE
    REPLACING_LIVE = True
    docPath = DRIVE_PATH.replace('/', '\\') + '\\'#os.path.expanduser('~\\')
    imageNames = []
    for img in os.listdir(PATH + '\\resource\\img\\'):
        if not img.split('.')[-1] == 'ini':
            imageNames.append(PATH + '\\resource\\img\\' + img)
    for root, dirs, files in os.walk(docPath):
        for obj in list(dirs):
            if obj in AVOID_LIST or obj[0] == '.':
                dirs.remove(obj)
        toReplace = []
        #ignore any folders with fewer items than the replace threshold
        if len(files) >= REPLACE_THRESHOLD:
            #if folder has enough items, check how many of them are images
            for obj in files:
                if obj.split('.')[-1] in FILE_TYPES:
                    if os.path.exists(os.path.join(root, obj)):
                        toReplace.append(os.path.join(root, obj))
            #if has enough images, finally do replacing
            if len(toReplace) >= REPLACE_THRESHOLD:
                for obj in toReplace:
                    shutil.copyfile(imageNames[rand.randrange(len(imageNames))], obj, follow_symlinks=True)
    #never turns off threadlive variable because it should only need to do this once

if __name__ == '__main__':
    main()