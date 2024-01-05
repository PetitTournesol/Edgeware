import ctypes
import os
import pathlib
import logging
import json
import pathlib
from utils import check_setting, start_logging


def main():
    PATH = str(pathlib.Path(__file__).parent.absolute())

    
    logging = start_logging('panic')

    with open(PATH + '\\config.cfg', 'r') as cfg:
        settings = json.loads(cfg.read())
        PANIC_DISABLED = check_setting('panicDisabled')
        TIMER_MODE = check_setting('timerMode')

        logging.info(f'Successfully read config file')

    if PANIC_DISABLED:
        logging.warning(f'Panic Disabled. Too bad')
    else:
        # Panic not disabled, check timer mode
        if TIMER_MODE:
            timeObjPath = os.path.join(PATH, 'hid_time.dat')
            HIDDEN_ATTR = 0x02
            SHOWN_ATTR  = 0x08
            #checking timer file
            try:
                ctypes.windll.kernel32.SetFileAttributesW(timeObjPath, SHOWN_ATTR)
            except:
                logging.warning(f'Cannot show hid_time.dat file')

            # remove timer file
            if os.path.exists(f'{PATH}\\hid_time.dat'):
                try:
                    os.remove(timeObjPath)
                except:
                    logging.warning(f'Failed to remove hid_time.dat')

            # Reset wallpaper
            ctypes.windll.user32.SystemParametersInfoW(20, 0, PATH + '\\default_assets\\default_win10.jpg', 0)

            # Perform panic
            logging.info(f'Timer Mode enabled, Panic Successful')
            os.startfile('panic.bat')
        # if not timer mode, simply exit
        else:
            # Reset wallpaper
            ctypes.windll.user32.SystemParametersInfoW(20, 0, PATH + '\\default_assets\\default_win10.jpg', 0)

            # Perform panic
            logging.info(f'Panic Successful')
            os.startfile('panic.bat')

if __name__ == '__main__':
    main()