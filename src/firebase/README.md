This repo holds the firebase code for connecting.

The only script you should run is [control.py](control.py) which takes as input the following arguments:
- A mandatory path to the firebase credential file
- a mandatory mode, either 'pc' to run on pc or 'rpi' to run on raspberry
- an optional database url, default is: `--databaseUR https://ledypie.firebaseio.com/`
- an optional number of pixels (this is the pixels your strip is made of), default is: `--pixels 300`
- an optional debug argument, with : `--debug`
- an optional type of strip with : `--strip_type`. Can be either `neopixel` or `dotstar`