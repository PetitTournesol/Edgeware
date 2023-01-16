import time
import os
import pathlib
from pypresence import presence

status_path = os.path.join(str(pathlib.Path(__file__).parent.absolute()), 'resource', 'discord.dat')
textObj = ['[No discord.dat resource]', 'default']

IMGID_CONSTS = ['furcock_img', 'blacked_img', 'censored_img', 'goon_img', 'goon2_img', 'hypno_img', 'futa_img',
                'healslut_img', 'gross_img']

# grab discord status from discord.dat, mark as having file
with open(status_path, 'r') as f:
    txt = f.read()

# if has file, tries to split at newline break
#   uses first line as the string for text description
#   uses second line as the image id for requesting image from discord api
ls = txt.split('\n')
textObj[0] = ls[0]
if len(ls) != 1:
    if ls[1] in IMGID_CONSTS:
        textObj[1] = ls[1]


# open discord api pipe and such
def do_discord():
    conn = presence.Presence('820204081410736148')
    conn.connect()
    conn.update(state=textObj[0], large_image=textObj[1], start=int(time.time()))
    while True:
        # Presence will auto-update while thread is live, so maintain until program is closed.
        time.sleep(15)


do_discord()
