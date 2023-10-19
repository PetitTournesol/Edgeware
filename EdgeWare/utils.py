import os
import json
import pathlib
import time
import logging

PATH = str(pathlib.Path(__file__).parent.absolute())
os.chdir(PATH)

def check_setting(name:str, default:bool=False) -> bool:
    
    with open(PATH + '\\config.cfg', 'r') as cfg:
        settings = json.loads(cfg.read())
    default = False if default is None else default
    try:
        return int(settings.get(name)) == 1
    except:
        return default

def start_logging(file_name:str) -> logging:
    #starting logging
    if not os.path.exists(os.path.join(PATH, 'logs')):
        os.mkdir(os.path.join(PATH, 'logs'))
    logging.basicConfig(filename=os.path.join(PATH, 'logs', time.asctime().replace(' ', '_').replace(':', '-') + '-' + file_name+ '.txt'), format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info('Started ' + file_name + ' logging successfully.')
    return logging