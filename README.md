# Edgeware
Elsavirus inspired fetish tool, built from the ground up to use interchangeable packages for better user experience.

Much like Elsavirus and Doppelvirus, this program was written in brainlet level Python, but unlike the two of them, was written ENTIRELY in Python. If you're the type to fear some hidden actually malicious scripts, this ensures that *all* of the code is front and center; no C++ forms or other tricks that might hide the true nature of the application.


The software features the popups, hard drive filling, porn library replacing, website opening features of its relatives.


Edgeware *does* include some unique features to make it more widely applicable than just the previous respective target demographics of /beta/ participants and finsub followers. Namely the packaging system, which allows anyone to cater to their own particular interests or fetishes. Either place a properly assembled zip file named "resources.zip" in the same folder as the scripts so that the program can unpack it or manually extract the resources folder into the said directory.

I more or less went into this wanting to make my own version of Elsavirus/Doppelvirus for fun, but figured around halfway that it might be worthwhile to share it with others who might have similar tastes.

Obviously you need to have Python installed, but other than that there should be no dependencies that aren't natively packaged with the language itself.

Premade Packages:
  Blacked:
    
    (TODO: add link)
  Male Yiff:
    
    (TODO: add link)
  Censored:
    
    (TODO: add link)

**Packages**
  Packages must be structured as follows:
  
    resources.zip
      ->resource
        ->aud
          (Audio Files) (Optional)
        ->img
          (Image Files)
        ->vid
          (Video Files) (Optional)
        icon.ico
        wallpaper.png
        web.json
   
  The web.json file should contain two sets:
  
    {"urls":["url1", "url2", ...], "args":["arg1,arg2,arg3", "", "arg1,arg2", ...]}
    ->urls - set of urls
    ->args - corresponding set of arguments; even if a url should take no argument, there must be a "" in this
      ->args are separated by commas within their strings, eg "arg1,arg2,arg3"
      ->ensure that urls and args are aligned; if the first URL can take the args "a,b" the first args value should be "a,b"
      ->args will be selected randomly and appended to the end of the url
        ->eg, "https://www.google.com/" with args "penis,cock,ass" cound randomly return one of 
        ->https://www.google.com/penis  https://www.google.com/cock  https://www.google.com/ass

If resources are not properly structured, the application could crash or exhibit strange behavior.

**Questions**

  "What about screenrape/writing prompts/Discord 'currently playing' integration?"
    I'll probably get around to adding them eventually; personally I wasn't the biggest fan of the writing prompts but since there are actual settings for Edgeware they'll probably end up being toggleable options in the future.

  "What new features are planned?
    Nothing really, I just intended for this to be a silly fetishware program for use by people whose interests are similar to mine. I'll probably update it here and there but new features aren't a priority.
