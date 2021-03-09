# Edgeware
**First and foremost as a disclaimer: this is NOT actually malicious software. It is intended for entertainment purposes only. Any and all damage caused to your files or computer is _YOUR_ responsibility. If you're worried about losing things, BACK THEM UP.**

FOR THOSE WHO DON'T CARE ABOUT GOING THROUGH THE CODE:


https://www.dropbox.com/s/4snjwtw1w6kmyds/edgeware_exe.zip?dl=0
    
    
Zip contains the set of compiled scripts. It runs slower than the raw .pyw files, but it doesn't require any additional effort to install Pillow that the raw files require. (Also in my experience AVG flags a false positive on them when they try to run, that's pyinstaller's fault, and I don't know how to fix it :^) )

Version 1.1.0 Updates:

    ->Updated config.cfg handling to use JSON for ease of use and ease of future updates.
      ->If you have used previous versions, either start in a new folder or erase your old config.cfg file before starting config.pyw or start.pyw
    ->Added ability to play audio in the background (AUDIO FILES IN /resource/aud/ MUST BE .WAV)
    ->Added "panicbutton.bat" as an emergency panic button so that you don't need to scroll through Task Manager or shut off PC to turn off EdgeWare.
      ->If you're in it for that thrill, feel free to just delete the batch file.
    ->Implemented the "Type out this prompt" feature, and a new resource "prompt.json" in the resource folder.
      ->An example prompt.json is provided in the new "example assets" folder.

(Pillow library is included; it's unmodified, but if you don't want to use the provided one, feel free to use "pip install pillow" to download a fresh copy)

Edgeware is an Elsavirus inspired fetish tool, built from the ground up to use interchangeable packages for better user experience.

Much like Elsavirus and Doppelvirus, this program was written in brainlet level Python, but unlike the two of them, was written ENTIRELY in Python. If you're the type to fear some hidden actually malicious scripts, this ensures that *all* of the code is front and center; no C++ forms or other tricks that might hide the true nature of the application.


The software features the popups, hard drive filling, porn library replacing, website opening features of its relatives.


Edgeware *does* include some unique features to make it more widely applicable than just the previous respective target demographics of /beta/ participants and finsub followers. Namely the packaging system, which allows anyone to cater to their own particular interests or fetishes. Either place a properly assembled zip file named "resources.zip" in the same folder as the scripts so that the program can unpack it or manually extract the resources folder into the said directory.

I more or less went into this wanting to make my own version of Elsavirus/Doppelvirus for fun, but figured around halfway that it might be worthwhile to share it with others who might have similar tastes.

Obviously you need to have Python installed, but other than that there should be no dependencies that aren't natively packaged with the language itself.

Premade Packages:

  Blacked:
  
  https://www.dropbox.com/s/fxibxo4joi9j7z1/blacked-resources.zip?dl=0
  
  Yiff:
  
  https://www.dropbox.com/s/t9sc6nr9jwhjn7s/yiff-resources.zip?dl=0
  
  Censored:
  
  https://www.dropbox.com/s/c0cpx79tf8g9pp8/censored-resources.zip?dl=0

**Packages**

  Packages must be structured as follows:
  
    resources.zip
       ->aud
         (Audio Files) (Optional)
       ->img
         (Image Files)
       ->vid
         (Video Files) (Optional) (Currently unused)
       icon.ico
       wallpaper.png
       web.json (Optional)
       prompt.json (Optional)
   
  The web.json file should contain two sets:
  
    {"urls":["url1", "url2", ...], "args":["arg1,arg2,arg3", "", "arg1,arg2", ...]}
    ->urls - set of urls
    ->args - corresponding set of arguments; even if a url should take no argument, there must be a "" in this
      ->args are separated by commas within their strings, eg "arg1,arg2,arg3"
      ->ensure that urls and args are aligned; if the first URL can take the args "a,b" the first args value should be "a,b"
      ->args will be selected randomly and appended to the end of the url
        ->eg, "https://www.google.com/" with args "penis,cock,ass" cound randomly return one of 
        ->https://www.google.com/penis  https://www.google.com/cock  https://www.google.com/ass
        
  The prompt.json file should contain any number of sets:
  
    {"moods":["mood1", "mood2", "angryMood"], "freqList":[10, 40, 50], "minLen":2, "maxLen"=4, "mood1":["mood1 sentence 1.", "mood1 sentence 2."], "mood2":["mood2 only has 1 sentence."], "angryMood":["angryMood also has one sentence."]}
        ->moods - names don't matter, as long as they're accounted for later in the set.
        ->freqList - correspond to each value in moods, define the frequency of that mood being selected.
        ->min/maxLen - minimum number of sentences that can be selected vs maximum.
        ->mood name
            ->can contain any number of mood related sentences.
            ->will ONLY select from this set if that mood is selected.
            
If resources are present, but not properly structured, the application could crash or exhibit strange behavior.

**Questions**

Q:  "What about screenrape/writing prompts/Discord 'currently playing' integration?"
  
   A: I'll probably get around to adding them eventually; personally I wasn't the biggest fan of the writing prompts but since there are actual settings for Edgeware they'll probably end up being toggleable options in the future.

Q:  "What new features are planned?
  
   A: Nothing really, I just intended for this to be a silly fetishware program for use by people whose interests are similar to mine. I'll probably update it here and there but new features aren't a priority.
