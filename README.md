# Edgeware
**First and foremost as a disclaimer: this is NOT actually malicious software. It is intended for entertainment purposes only. Any and all damage caused to your files or computer is _YOUR_ responsibility. If you're worried about losing things, BACK THEM UP.**


Version 1.1.4 Updates (1.1.3 included):

    (1.1.3)
        ->Config file now updates automatically between versions, no need to create a new one every time.
        ->Prompts now properly wrap their text to fit the text box.
        ->get-pip.pyw is now included with the download.
        ->On first run, the program will attempt to install python package installer, and then install python image library using it
            ->This is to ensure that the popups work correctly, as tkinter doesn't like to play nice with non-JPG images without PIL.
        ->On subsequent runs it shouldn't attempt to reinstall.
        ->Now runs config.pyw before the virus actually runs for the first time!
            ->On subsequent runs it will jump directly into the actual application, so use config.pyw in the folder manually beyond that.
        
    (1.1.4)
        TODO for 1.2.0: Lots and lots of error catching, expect program to no longer fail silently but instead scream to the heavens when something breaks.
        -> Bugfix in startup, now properly uses "py -m pip install pillow" as default method of installing
        -> Bugfix for config not properly writing config.cfg properly.
        -> Added defaultConfig.dat for consistency across future options updates.
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
