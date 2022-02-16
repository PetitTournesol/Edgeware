@echo off
:top
echo Which feature would you like to run?
echo 1: Start.pyw (Edgeware)
echo 2: Popup.pyw (Popup only)
echo 2a: Popup.pyw (Video only)
echo 3: Config.pyw (Config)
set /p usrSelect=Select number:
if %usrSelect%==1 goto startLbl
if %usrSelect%==2 goto popupLbl
if %usrSelect%==2a goto popup2Lbl
if %usrSelect%==3 goto configLbl
echo Must enter selection number (1, 2, 3)
pause
goto top
:startLbl
echo Running start.pyw...
py start.pyw
echo Done.
pause
goto quitLbl
:popupLbl
echo Running popup.pyw...
py popup.pyw
echo Done.
pause
goto quitLbl
:popup2Lbl
echo Running popup.pyw...
py popup.pyw -video
echo Done.
pause
goto quitLbl
:configLbl
echo Running config.pyw
py config.pyw
echo Done.
pause
:quitLbl
echo Goodbye!