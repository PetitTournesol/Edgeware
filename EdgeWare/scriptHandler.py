import os
import time
import winsound
import threading as thread
import sys
import random as rand
import webbrowser
from tkinter import Tk, Label, Frame, Button

SYS_ARGS = sys.argv

PATH = os.curdir

class ScriptHandler:
    def __init__(self, script_name):
        self.bookmarks = dict[str, int]({})
        self.scriptLiteral = []
        self.argList = []
        self.ans = None
        self.rCount = 0
        self.currentLine = 0

        #dict of str -> function
        #used to make new operations easier to add and old ones easier to adjust
        self.lib = {
            'bookmark' : lambda: print(self.scriptLiteral[self.currentLine]),
            'jump'     : lambda: self.jump(self.argList[0]),
            'showImg'  : lambda: self.showImg(self.argList[0]),
            'showText' : lambda: self.showText(self.argList[0], self.argList[1]),
            'showOpt'  : lambda: self.showOpt(self.argList[0], self.argList[1], self.argList[2]),
            'playAud'  : lambda: self.playAud(self.argList[0]),
            'repeat'   : lambda: self.jumpR(self.argList[0], int(self.argList[1])),
            'wait'     : lambda: time.sleep(float(self.argList[0])),
            'waitR'    : lambda: self.waitRand(self.argList[0], self.argList[1]),
            'switch'   : lambda: self.jumpS(self.argList[0], self.argList[1]),
            'openWeb'  : lambda: webbrowser.open(self.argList[0])
        }

        with open(os.path.join('scripts\\', script_name)) as file:
            self.raw_script = [line.rstrip('\n') for line in file.readlines()]
            
            #locates the start of the script, dies if cant find start
            while self.raw_script[0] != '<script>':
                self.raw_script.pop(0)
                if len(self.raw_script) == 0:
                    print('could not parse script, no start point. exiting.')
                    exit(0)

            #locates end of script, dies if can't find it
            while self.raw_script[len(self.raw_script)-1] != '</script>':
                self.raw_script.pop()
                if len(self.raw_script) == 0:
                    print('could not parse script, fell of edge. exiting.')
                    exit(0)

            #removing the <script> and </script>
            self.raw_script.pop(0)
            self.raw_script.pop()

            self.scriptLiteral = self.raw_script

            #making dict of bookmarks
            for line in self.scriptLiteral:
                if line.startswith('bookmark '):
                    self.bookmarks[line.split(' ')[1]] = self.scriptLiteral.index(line)

    #jumps to given bookmark, does nothing if no bookmark of given name exists
    def jump(self, target) -> None:
        try:
            self.currentLine = self.bookmarks[target]
        except:
            print('unrecognized bookmark')

    #"jumpRepeat", alternate jump for repeating jump operation
    #please god dont nest these it will almost certainly fuck everything up
    #like
    #really bad
    #please dont do it
    #c:
    def jumpR(self, target, count) -> None:
        if self.rCount <= count:
            self.jump(target)
            self.rCount += 1
        else:
            self.rCount = 0

    #"jumpSwitch", alternate jump for the switch operation
    def jumpS(self, target1, target2) -> None:
        self.jump(target1) if self.ans == 0 else self.jump(target2)

    #displays given image name with popup.pyw
    #using name %RAND% will result in random image being selected
    #tags:
    #   async   - start popup asynchronously to other commands
    #   timeout - force popup timeout, "timeout=number"
    #   showCap - show caption, ignoring settings 
    #   hideCap - hide caption, ignoring the settings (this takes precedence over show)
    #   mitosis - force mitosis mode, "mitosis=number"
    def showImg(self, name) -> None:
        argStr = (self.tagToArg('timeout') + 
                  self.tagToArg('showCap') + 
                  self.tagToArg('hideCap') + 
                  self.tagToArg('mitosis'))

        if not self.checkTag('async'):
            os.system(r'python popup.pyw ' + name + argStr)
        else:
            thread.Thread(target=lambda: os.system(r'python popup.pyw ' + name + argStr), daemon=True).start()

    #wait random time between lowlim and hilim, ints only
    def waitRand(self, lowLim, hiLim):
        time.sleep(rand.randint(int(lowLim), int(hiLim)))

    #displays text window
    def showText(self, title, text):
        self.rootOpt = Tk()
        self.rootOpt.title(title)
        self.rootOpt.geometry('200x150')
        self.rootOpt.resizable(False, False)
        self.rootOpt.attributes('-toolwindow', 1)
        self.plb = Label(self.rootOpt, text=text, wraplength=190)
        self.plb.pack(side='top', fill='both', expand=1)
        self.rootOpt.mainloop()

    #displays text window with 2 option buttons, response is stored in self.ans and can be immediately applied
    #by using the switch expression immediately after 
    def showOpt(self, prompt, opt1, opt2) -> int:
        self.rootOpt = Tk()
        self.rootOpt.title('Choice')
        self.rootOpt.geometry('200x150')
        self.rootOpt.resizable(False, False)
        self.rootOpt.attributes('-toolwindow', 1)
        self.plb = Label(self.rootOpt, text=prompt, wraplength=190)
        self.bPn = Frame(self.rootOpt)
        self.ob1 = Button(self.bPn, text=opt1, command=lambda:select(0))
        self.ob2 = Button(self.bPn, text=opt2, command=lambda:select(1))
        def select(val):
            self.rootOpt.destroy()
            self.ans = val
        self.plb.pack(side='top', fill='both', expand=1)
        self.bPn.pack(side='bottom', fill='x')
        self.ob1.pack(side='left', fill='x', expand=1)
        self.ob2.pack(side='right', fill='x', expand=1)

        self.rootOpt.mainloop()

    #plays audio
    #tags:
    #   async - play audio async to other script commands
    def playAud(self, name) -> None:
        if self.checkTag('async'):
            thread.Thread(target=
                            lambda: winsound.PlaySound(os.path.join('resource\\aud\\', name), winsound.SND_FILENAME),
                        daemon=True
                        ).start()
        else:
            winsound.PlaySound(os.path.join('resource\\aud\\', name), winsound.SND_FILENAME)

    #parses arglist based on quotation grouping (playaud "file name.wav" -> self.playAud("file name.wav"))
    def parseMultipartText(self):
        self.parsedList = []
        concatMode = False
        workStr = ''

        for arg in self.argList:
            if arg.startswith('"') and not concatMode:
                concatMode = True
                arg = arg.lstrip('"')
            if arg.endswith('"') and concatMode:
                concatMode = False
                arg = arg.rstrip('"')
            workStr += arg + (' ' if concatMode else '')
            if not concatMode:
                self.parsedList.append(workStr)
                workStr = ''
        self.argList = self.parsedList
    
    #checks info from tagList
    def checkTag(self, text) -> bool:
        for tag in self.tagList:
            if tag.startswith(text):
                return True
        return False

    #seeks tag and returns the full tag text (seeking "mitosis" will return "mitosis=value")
    def seekTag(self, text) -> str:
        for tag in self.tagList:
            if tag.startswith(text):
                return tag
        return ''

    #returns arg string of tag if present, used for string building args for command runs
    def tagToArg(self, text):
        return (' ' + self.seekTag(text) if self.checkTag(text) else '')

    #executes current line and moves line point down the script by 1 space
    def executeLine(self):
        #allows for comments starting with #
        if self.scriptLiteral[self.currentLine].startswith('#'):
            self.currentLine += 1
            return
        
        try:
            self.argList = self.scriptLiteral[self.currentLine].split(' ')
            self.parseMultipartText()
        except:
            self.argList = [self.scriptLiteral[self.currentLine]]

        try:
            self.tagList = self.argList[self.argList.index('-tags') + 1].split(' ')
        except:
            self.tagList = []
        
        self.command = self.argList.pop(0)
        self.lib[self.command]()
        self.currentLine += 1

    #executes current line as long as the line has not reached the end of the script
    #after end of file is reached, kills program
    def execute(self):
        while self.currentLine < len(self.scriptLiteral):
            self.executeLine()
        print('finished, fell of script end')
        os.kill(os.getpid(), 9)

#TODO: REPLACE WITH SYS_ARGS[1] AFTER TESTING
handler = ScriptHandler('test_script.horny')
handler.execute()