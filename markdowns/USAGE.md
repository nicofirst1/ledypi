## RaspberryPi

### Testing
You can use the [test script](src/rpi/test.py) to run a specific pattern without the connection to firebase.

First source the python path with:
```shell script
source scripts/app.sh  
```

Then run the test with:
```shell script
sudo python src/rpi/test.py PatternName 
```

### Remote

You can test the remote configuration running the [control](src/firebase/control.py) script which takes as **mandatory** inputs 
the credential json file and the mode (either 'pc' or 'rpi') which specify where the script is being run.

```shell script
python src/firebase/connect.py credential.json rpi
```
To run it on the RaspberryPi.



## PC
To test first run the [gui](src/pc/gui.py) and then in a separate process run [patterns](./src/pc/test.py)
```shell script
python src/pc/gui.py
python src/pc/test.py
```

For the remote connection use:
```shell script
python src/gui.py
python src/firebase/connect.py credential.json pc
```



## Additional params
The [control script](src/firebase/control.py)  accepts two optional arguments:
- _databaseURL_ : the url of your database (default [value](https://ledypie.firebaseio.com/), more in the [firebase tutorial](https://rominirani.com/tutorial-mit-app-inventor-firebase-4be95051c325))
- _pixels_ : the number of pixels (default 300).

To connect to a custom databaseURL with 64 leds on the rpi you should run

```shell script
python src/firebase/connect.py credential.json rpi --databaseURL https://customURL.firebaseio.com/ --pixels 64
```
