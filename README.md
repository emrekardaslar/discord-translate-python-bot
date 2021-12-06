# discord-translate-python-bot
Basic python bot to listen any language supported by Google Translate. 

To use, type !t language "desired sentence". For example: 

!t en "Hello World"

!t fr "Général Kenobi"

# Libraries needed to be installed: 
Install libraries by:
```
pip install -r requirements.txt
```
Additionally

```
pip install PyAudio
```

If you face problems installing PyAudio on Windows:

Download pyaudio wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/ and pip install.

(https://stackoverflow.com/questions/53866104/pyaudio-failed-to-install-windows-10/53866322)


# Additional Features

* Can get the forecast data by using !w city_name command (like !w texas)
* Can get covid data by using !covid country_name
* Can get currency data by using !cur amount cur-from cur-to
