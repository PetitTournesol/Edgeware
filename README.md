# Edgeware
**First and foremost as a disclaimer: this is NOT actually malicious software. It is intended for entertainment purposes only. Any and all damage caused to your files or computer is _YOUR_ responsibility. If you're worried about losing things, BACK THEM UP.**

Version 2.1.1 Updates

**(2.1.1)**

   _**[New Additions]**_
   
•**Import** *Config now has a manual resource zip import button*

•**Alerts** *Added additional alert dialogs*

   _**[Updated Features]**_

•**Multi monitors** *Popups now appear on all monitors, instead of just the main monitor*

   _**[Bugfixes]**_
   
•**Paths** *Updated path fetch functions, should now avoid System32 Permission Denied errors due to incorrect path fetching*

**(2.1.0)**

   _**[New Additions]**_
   
•**Panic! Panic!** *Panic button now has a proper, assignable button associated with it (this only works when pressed while a prompt is in focus). Panic button also now restores wallpaper to the Windows 10 default instead of leaving it be*

•**Captions** *Prompts now have basic caption support; this feature is toggleable and currently unused. Packs will be updated within the coming weeks to include captions. (An empty captions.json file will be in example assets)*

•**Updates** *Config now has a version checking feature; if the local version and the version listed on Github are differet it will alert you with a popup and the version display at the bottom left will be red.*

•**What zip?** *Config now has a section at the bottom left that tells you what zip file start will select to unpack.*

   _**[Updated Features]**_
   
•**Custom Images** *Improved Discord integration to use custom images; these are only able to be pulled from a select number of pre-cached images with certain codes. Default packs will be updated to reflect this with the pack caption update.*

•**Threads** *The maxFillThread variable to manage hard drive fill speed has been added to the advanced section of the config menu. Be careful adjusting this if you don't know what you're doing.*
        
   _**[Bugfixes]**_

•**Borders** *Popup windows now properly show their borders all the way around the image.*

•**Disk Skipping** *Fill drive no longer skips avoiding every other non-useable folder in the directory.*

_**[How to Use]**_

Start by downloading this repository as a zip, and then extracting it somewhere on your computer.

(*If not using a premade package, skip this step.* )
Download one of the premade packages listed below. Once it's downloaded (if using a premade package), place it into the Edgeware folder inside Edgeware-main. 

Ensure that you have a recent installation of Python 3 (3.9+ is preferred).

Finally, double click to run start.pyw. If it's your first time running the program in that directory, it will install PIP (https://www.w3schools.com/python/python_pip.asp) and use it to perform some library installations to ensure proper functionality. After this is complete, the Config menu will appear. Configure the settings to your liking and save. Finally, Edgeware proper will start. Enjoy!


   _**[Premade Packages]**_

**Blacked**

*Standard Blacked hentai stuff, includes Porn Addict Brainwash Program: BBC Edition, and some volafile mp3s from /trash/ Blacked threads*

https://drive.google.com/file/d/1BHLrCO5cvm9YCF_EeWGYS8AmAsPxUZPJ/view?usp=sharing

**Gay Yiff**

*Includes lots and lots of steamy, hulking furry cocks*

https://drive.google.com/file/d/1b2gOJBLy-nD5p1cOM8xTDPh7LGsf1g58/view?usp=sharing

**Censored**

*For the people who get off to not getting off*

https://drive.google.com/file/d/1phBN4JhoyOg3yAMomGgIKVTryYc8dv4Q/view?usp=sharing

**Hypno**

*Includes the most gifs of any pack by far, as well as Porn Addict Brainwash Program 5 & 6, and Queue Balls 1*

https://drive.google.com/file/d/1W2u_wAp2DAWa-h0O5VUlGKhKSVMwQkh5/view?usp=sharing

**Gooner**

*Includes the same audio as Hypno, as well as an MLP worship themed hypnosis file by https://twitter.com/AlmondMilkomg. Fair warning, most things are fair game for this one, including furry, farts, cringe, ponies, etc.*

https://drive.google.com/file/d/1GhJQ7OtL9hblQJ4NTLP3Nz23AKcUqdz-/view?usp=sharing

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
