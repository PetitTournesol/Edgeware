# Edgeware
**First and foremost as a disclaimer: this is NOT actually malicious software. It is intended for entertainment purposes only. Any and all damage caused to your files or computer is _YOUR_ responsibility. If you're worried about losing things, BACK THEM UP.**

Version 2.0.0 Updates [WIP]
        
   _**[New Additions]**_
   
•**GIF support in popups** *Animated GIFs in the /resource/img/ folder now properly animate in their popups*
        
•**Hibernation Mode** *New operation mode; Edgeware will sit dormant for a random, configurable amount of time before shooting a lewd load all over your screen and returning to sleep to do it again later*

•**Discord Integration** *Now shows in "Currently Playing" on Discord, this feature is toggleable and has different flavor text for every pack*

•**Run On Startup** *Now has an option to start on computer startup*

•**Shortcut Creation** *Now creates shortcuts for Edgeware, Config, and Panic Button on the Desktop*

•**Resource Exporting** *Want to share your custom pack but not sure how to package it? Config menu now has a button to automatically export a properly configured zip with all of your resource folder!*

•**Default Assets** *Now handles missing resources better, using items from the default_asset folder if a zip can't be found; in other words, if you just want to create your own pack from the ground up, running start without a zip file in the Edgeware folder will generate an empty resource zip template*

•**2 New Image Packs** *Find the download links below*

   _**[Updated Features]**_
   
•**Config Menu** *Config menu has been completely reworked, now including an Advanced Options section and an About section, also can now be started without running start.pyw first*

•**resources.zip** *When importing resources, now selects the alphebetically earliers zip file in the Edgeware folder instead of requiring a specific zip name*

•**Fill Naming** *Now uses hashed value when creating files for "fill drive" instead of os.time raw data*

•**Oops, something broke** *Now has better error handling in cases of common issues like missing or misconfigured resources*

•**Old Resources** *All 3 original resource packs have been updated with new content, as well as now containing both prompt.json and web.json*
        
   _**[Bugfixes]**_

•**Settings** *Now properly applies settings on the first run instead of requiring a program restart*

•**Filled Quick** *Now properly applies the fill_delay variable, which was previously inert due to a small conditional oversight*

   _**[Premade Packages]**_

**Blacked**

*Standard Blacked hentai stuff, includes Porn Addict Brainwash Program: BBC Edition, and some volafile mp3s from /trash/ Blacked threads*

~Link Here~
  
**Gay Yiff**

*Includes lots and lots of steamy, hulking furry cocks*

~Link Here~
  
**Censored**

*For the people who get off to not getting off*

~Link Here~

**Hypno**

*Includes the most gifs of any pack by far, as well as Porn Addict Brainwash Program 5 & 6, and Queue Balls 1*

~Link Here~

**Gooner**

*Includes the same audio as Hypno, as well as an MLP worship themed hypnosis file by https://twitter.com/AlmondMilkomg, fair warning, most things are fair game for this one, including furry, farts, cringe, ponies, etc.*

~Link Here~

__**What is Edgeware?**__

Edgeware is an Elsavirus inspired fetishware tool, built from the ground up to use interchangeable resource packages for easily customized user experience.

Much like Elsavirus and Doppelvirus, this program was written in brainlet level Python, but unlike the two of them, was written ENTIRELY in Python. If you're the type to fear some hidden actually malicious scripts, this ensures that *all* of the code is front and center; no C++ forms or other tricks that might hide the true nature of the application.


The software features the popups, hard drive filling, porn library replacing, website opening features of its predecesors.

Edgeware *does* include some unique features to make it more widely applicable than just the previous respective target demographics of /beta/ participants and finsub followers. Namely its packaging system, which allows anyone to cater the experience to their own particular interests or fetishes. Either place a properly assembled zip file named "resources.zip" in the same folder as the scripts so that the program can unpack it or manually extract the resources folder into the said directory.

I more or less went into this wanting to make my own version of Elsavirus/Doppelvirus for fun, but figured around halfway that it might be worthwhile to share it with others who might have similar tastes.

Obviously you need to have Python installed, but other than that there should be no dependencies that aren't natively packaged with the language itself.

__**Packages**__

  Packages must be structured as follows:
  
    (name).zip
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

*(If you like my work and would like to help me pay for food, please feel free to donate; Cashapp is $PetitTournesol)*
