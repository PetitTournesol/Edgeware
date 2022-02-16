
# Edgeware
**First and foremost as a disclaimer: this is NOT actually malicious software. It is intended for entertainment purposes only. Any and all damage caused to your files or computer is _YOUR_ responsibility. If you're worried about losing things, BACK THEM UP.**

If you get error "TypeError: unsupported operand type(s) for |: 'type' and 'type'", please make sure your Python is up to date! This version was primarily developed on Python 3.10.2!

Version 2.4.1 Update

•*Fixed bug where start and config would crash on startup for new users due to PIL not being properly placed into the safe import blocks*

Version 2.4.0 Updates

   _**[Large Additions]**_
   
•**Timer Mode** *Timed runs can now be set, during which the Panic features cannot be used (unless a password is set and used). Run on startup is also forcibly enabled during this time.*

•**Mode Presets** *Config files can now be saved as "Presets," and can be freely swapped between in the config menu itself. These can have descriptions along with them, stored as [preset name].txt text files inside the preset folder.*

•**Lowkey Mode** *A more laid back way to enjoy Edgeware, but more active than Hibernate Mode. Popups will flash from corner to corner before slowly fading away and being replaced by another new popup.*

•**Denial Mode** *While Denial Mode is toggled, popups can randomly be blurred out or otherwise censored. Text will appear on top of them, either a default phrase or a phrase selected from the captions.json file under the "denial" tag.*

•**Popup Subliminals** *Popups can now have subliminal gifs overlayed on top of them. To accompany this, a "submliminals" folder is now supported in resource packs, from which a subliminal gif will be randomly selected and overlayed on top of the image. If none are present, the default gif in default_resources will be used.*

     •*Please be aware that this feature can potentially be very memory/cpu intensive and set your popup fadeout accordingly.*

•**Booru Downloader Update** *The previous booru downloader was incompatible with Rule34, and had actually completely broken due to a Booru update. The new version is more efficient and easier to maintain/fix if the issue arises again, and is also now able to handle exceptions to standard Booru URLs like Rule34.*

  _**[Small Additions]**_
  
•**Logging** *Start, config, and popup now all generate log files detailing their operation and any errors they encounter with greater detail.*

•**Panic Wallpaper** *Panic wallpaper is now previewed in the config menu, and can be changed to an image of your choice there, under the wallpaper tab.*

•**Debug Tool** *For other errors/viewing of print statements, a small debug batch tool has been added.*

•**Popup Opacity** *Added a new opacity setting for popups.*

•**Tray Icon** *Added a tray icon for Edgeware, which allows you to easily use the panic feature even while no popups are on the screen without manually running the panic files.*

   _**[Updated Features]**_

•**Panic Button** *The panic button is now "e" by default instead of "\`".*

•**Fill Delay** *Updated fill delay setting, now ranges from 0ms to 2500ms instead of the previous 0-25ms.*

•**Video Player** *Videos no longer play in a web browser, and instead now play in popup windows. The volume of the videos can also be configured on the config menu.*

•**Audio Handling** *Updated how audio is played, so now mp3 OR wav files, probably others too but I haven't tested them.*

•**Wallpaper Handling** *Updated wallpaper handling, which should result in wallpapers being more stable for config to handle, and prevent any accidental self doxxing when sharing config files.*

•**Library Imports** *Updated library importing at the start of start and config. Much more standardized and no longer requires checks in the config file.*

•**Config Layout** *Config layout has been updated, with features being more spaced out.*

•**General Standardization** *Start and Config have been updated to make their code more standardized. (I did my best to comply with pep8 but I'm very stupid so please bear with me programmers)*

•**Advanced Tab** *Minor adjustments to the Advanced tab layout, bringing it into line with the rest of the config menu.*

   _**[Bugfixes]**_
   
•**Popup Borders** *Popups now properly have borders that go all the way around the image instead of just the top and left sides.*

•**Config/Start Crash** *Fixed bug where the config file would be corrupted by config.cfg saving wallpapers in a certain configuration.*

•**Wallpaper Crash** *Fixed bug where missing wallpaper setting would cause config to crash when opening.*

•**Run on Startup Failure** *Fixed bug where the startup bat would not be placed into the windows startup folder. (This should be fixed, but it's always possible I just fixed a different but connected issue instead.)*

   _**[Additional Note]**_**
   
Hello! This will likely be the last update (or at least, last main release version) of Edgeware for the time being. Unfortunately with the constraints of life and my declining interest in porn, it's become more and more difficult to maintain the project as I had originally planned to. It does make me very happy that so many people enjoy my work, and I hope that this update can at least make it feel a bit more complete for you all. I'm very thankful for all the kind words I've received regarding the project, and maybe one day I'll be back to make more updates, but for now I'll be focusing on life and other projects. I'll also be sporadically available on my Twitter to answer tech support questions or just chat. I love you all and please take care of yourselves! <3

_**[How to Use]**_

Start by downloading this repository as a zip, and then extracting it somewhere on your computer.

(*If not using a premade package, skip this step.* )
Download one of the premade packages listed below. Once it's downloaded (if using a premade package), place it into the Edgeware folder inside Edgeware-main. 

Double click "EdgewareSetup.bat" and follow the instructions. It should check your Python version, and then automatically download the correct installer from python.org and run it. Once you finish with that installation, it will run start.pyw, which will walk through an automated first time setup. Once this setup is complete, it will provide you with the config window to select your settings, and then run! (The installations only need to be performed on the first run)

   _**[Premade Packages]**_

**Blacked**

*Standard Blacked hentai stuff, includes Porn Addict Brainwash Program: BBC Edition, and some volafile mp3s from /trash/ Blacked threads*

https://drive.google.com/file/d/1BHLrCO5cvm9YCF_EeWGYS8AmAsPxUZPJ/view?usp=sharing

https://mega.nz/file/IfJS1JLB#eEkreHNBH5g_maKsiUC0I1BOeh1FvdOwU5i-Eto6FwA

**Gay Yiff**

*Includes lots and lots of steamy, hulking furry cocks*

https://drive.google.com/file/d/1b2gOJBLy-nD5p1cOM8xTDPh7LGsf1g58/view?usp=sharing

https://mega.nz/file/kOA2DZAJ#5A7pfQUdEKq8s3ner4dhmrKxS7xoYupMcNAAK3voU3M

**Censored**

*For the people who get off to not getting off*

https://drive.google.com/file/d/1phBN4JhoyOg3yAMomGgIKVTryYc8dv4Q/view?usp=sharing

https://mega.nz/file/lPBUxRyA#AJlC4Kwrtdci3cjISWkZ8YThuWEmyHcL81MfZoprrqQ

**Hypno**

*Includes the most gifs of any pack by far, as well as Porn Addict Brainwash Program 5 & 6, and Queue Balls 1*

https://drive.google.com/file/d/1W2u_wAp2DAWa-h0O5VUlGKhKSVMwQkh5/view?usp=sharing

https://mega.nz/file/YHB2ABAa#QApGJHeg6EF-20VP0OVf8yZyQtmCdZRQduXrHOHvUCM

**Hentai/Basic Gooner**

*Includes mostly 3D or hentai images, has 100% gifs, some videos, and audio from the porn addict brainwash program and queue balls*

https://drive.google.com/file/d/10_t11qm_2fRp4GVh0JK4hskdwW9ppCme/view?usp=sharing

https://mega.nz/file/gWwDmYJT#xWGsdfaPB5TvsnvDC4OUEWR06flqn7Bc9pvOErSUBuY

**No Limit Gooner**

*Includes the same audio as Hypno, as well as an MLP worship themed hypnosis file by https://twitter.com/AlmondMilkomg. Heavier focus on stranger kinks such as ponies, furry, farts, cringe, emoji, etc.*

https://drive.google.com/file/d/1nExnM00ODbZjAV2w8UX-Ybw8wp3ffNjK/view?usp=sharing

https://mega.nz/file/0SQEzZrb#UK6SSDUFz8u_xM5lcNMStqQdS-bqE_ilB6u7RkGUjGM

**Elsa**

*More or less all of the original assets and resources from the original Elsavirus. It's not a 1:1 experience, but if you liked the Elsa theming and original writing, it's all still there.*

*Warning that this pack does contain ALL of the resources from the original Elsavirus, including the noose image.*

https://drive.google.com/file/d/1QLJI52zM9HrJP_ozNxLaUSSEVUoDpjJP/view?usp=sharing

https://mega.nz/file/JKRCHR4a#SnxrAar_rvhK4BYjewz1TZmtV6EEeyEG9QU8JTkWOck

**Futanari**

*Futa themed pack, includes some generic moaning and plap plap audio. This and the Elsa pack are the first to make use of the caption feature, older packs will be updated with new resources and caption assets in the coming weeks.*

https://drive.google.com/file/d/12L9lKiOzKgBlDaoPudNhkYgZH-3khUeh/view?usp=sharing

https://mega.nz/file/AWQUTDYb#1rjRbHbDfqTVt-w7m-IryWFAf95us0tg3kBq-5VybGw


__**FAQ**__

**Q: "Why do I keep getting white circles in my popups?"**

**A: *This occurs when the resource folder is generated without any resource zip in the script folder. Either delete your resource folder and restart Edgeware with the zip located properly or manually import your zip with the config function.***

**Q: "Where does the booru downloader save files?"**

**A: *The booru downloader saves all files it downloads into the /resource/img/ folder.***


__**What is Edgeware?**__

Edgeware is an Elsavirus inspired fetishware tool, built from the ground up to use interchangeable resource packages for easily customized user experience.

Much like Elsavirus and Doppelvirus, this program was written in brainlet level Python, but unlike the two of them, has no compiled executables. If you're the type to fear some hidden actually malicious scripts, this ensures that *all* of the code is front and center; no C++/C# forms or other tricks that might hide the true nature of the application.


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
         (Image Files, Gif Files)
	   ->subliminals
	     (Gif files only) (Optional)
       ->vid
         (Video Files) (Optional)
       icon.ico
       wallpaper.png
       web.json (Optional)
       prompt.json (Optional)
	   discord.dat (Optional)
	   captions.json (Optional)
   
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
