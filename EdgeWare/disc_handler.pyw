from io import TextIOWrapper
import time, os
from tkinter import Image, PhotoImage
from pypresence import presence

status_path = os.path.join(os.path.abspath(os.getcwd()), 'resource', 'discord.dat')

textObj = '[No discord.dat resource]'
with open(status_path, 'r') as f:
    try:
        textObj=f.read()
    except:
        print('failed line split')


def do_discord():
    conn = presence.Presence('820204081410736148')
    conn.connect()
    conn.update(state=textObj, large_image='default', start=int(time.time()))
    while True:
        time.sleep(15)

do_discord()