# Build 
Follow the [BUILD file](BUILD.md) if you need to buy the components, set up the raspberryPi or connect the cables.

The following instructions regards the project installation only.
# Setup
This project uses these tools:
1. [DotStar_emulator](https://github.com/chrisrossx/DotStar_Emulator) to simulate the led strip on pc.
2. [AppInventor](http://appinventor.mit.edu/) for the android app build.
3. [Firebase](https://console.firebase.google.com/) to allow communication between web/android app and pc/raspberry.
4. [Adafruit_CircuitPython_NeoPixel](https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel) to control the leds on the raspberry.
5. [audio-reactive-led-strip](https://github.com/scottlawsonbc/audio-reactive-led-strip) to control leds with music.

Since the _DotStar_emulator_ cannot be installed on the raspberry and the _rpi-NeoPixel_ does not work on pc, this two libraries are kept well separated.

In the following I will guide you to the installation and setup required to make everything work

## Get the code on Raspberry
There are two ways to get the repo on your raspberry: cloning the repo or copying through ssh.

### Clone
If you just wish to use the project without implementing custom patterns use:
```shell script
git clone --recursive https://github.com/nicofirst1/ledypi
```
On your raspeberryPi

### Copy
On the other hand, if you would like to play with the repo, you should clone it on your PC with:
```shell script
git clone --recursive https://github.com/nicofirst1/ledypi
```
And then use the [sync script](../scripts) to copy the repo onto your RaspberryPi

## Python 3.7
The project works with python>=3.7, it is advised to source your custom env before proceeding.

### RaspberryPi

The [install script](../scripts/install.sh) should take care of most of the installation part, simply use:
```shell script
bash scripts/install.sh
```
If you run into any problems check out the full install instructions which follows.

#### Complete install instructions

- Install packages:
```shell script
sudo apt-get install python3-numpy 
```
- Install Blinka with the [tutorial](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)
- Install the required modules:
```sudo pip3 install -r requirements_pi.txt ```
- Install opencv:
    - install dependencies
    ```
    sudo apt-get install libhdf5-dev libhdf5-serial-dev
    sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
    sudo apt-get install libatlas-base-dev 
    sudo apt-get install libjasper-dev
    ```
    or in one line
    ```
      sudo apt-get install libhdf5-dev libhdf5-serial-dev libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5 libatlas-base-dev libjasper-dev
   ```
    - install opencv 
    ````
    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3 get-pip.py
    
    sudo pip3 install opencv-contrib-python==4.1.0.25
    ````
- Install Pillow:
```shell script
sudo apt-get install  libjpeg-dev zlib1g-dev libfreetype6-dev liblcms1-dev libopenjp2-7 libtiff5 
sudo pip3 install pillow

```
- (Optional) If you have a microphone connected to your Rpi follow the instructions in the [audio reactive readme](../audio-reactive-led-strip/README.md)
- (Optional) Increase led speed by adding following to `/boot/config.txt` ( as written [here](https://github.com/jgarff/rpi_ws281x/issues/381)):
```shell script
core_freq=500
core_freq_min=500
```                                         

If you get a gcc error see [this](https://stackoverflow.com/questions/20023131/cannot-install-pyaudio-gcc-error).

#### Ledyweb on raspberry
If you wish to run the ledyweb control server on the raspberry and connect with another pc you should follow
 [this guide](https://www.codingforentrepreneurs.com/blog/raspberry-pi-network-server-guide-with-django-ssh/)

##### Ledyweb on apache
If you rather have the ledyweb control directly running on the rpi, you can use the [apache_setup scrip](../scripts/apache_setup.sh). Simply run it with:
```shell script
bash scripts/apache_setup.sh
```

### PC

- Install the required modules:
```pip install -r requirements.txt ```
- (Optional, only if you wish to create custom patterns) install [DotStar_emulator repo](https://github.com/nicofirst/DotStar_Emulator) to debug Patterns on pc:
```
python DotStar_Emulator/setup.py install
```



## App Inventor
The MIT [AppInventor](http://appinventor.mit.edu/) is a tool to simply create apps with a building block programming paradigm. 
The first thing you'll need to do is make an account.
Then you can import the app from the [ledypi.aia](../AppInventor/ledypi.aia) file:
```
Click on 'Create Apps!'
Login
Click on 'My Projects' on the top left 
Import project (.aia) from my computer ...
And select the ledypie.aia file
```
Once imported you need to se the firebase URL and Token in 

```
Click on th "Designer" button on the top left
In the "Components" window scroll down unti you see  "FireBaseDB1" and click on it
Set both the "FirebaseToken" and "FirebaseURL"
```
Now you need to se the firebase url in the blocks too
```
Click on th "Blocks" button on the top left
Find the orange global initializer called "fire_base_url"
Set it to your url
```

You can check the [README](../AppInventor/README.md) in the AppInventor directory for more infos.

### Firebase
The communication between the app and python works through the [Firebase](https://console.firebase.google.com/) database.

#### Database creation and linking 
To create a Firebase database and link it to the app use 
[this tutorial](https://rominirani.com/tutorial-mit-app-inventor-firebase-4be95051c325) and follow the __Firebase Setup__ only, everything else is already implemented.
Be aware the FireBaseDB is already present in the app, so you don't need to instantiate a new one, simply fill out the _FirebaseToken_ and _FirebaseURL_ as described above.

#### Generating private key file
To connect the database with the python application you will need to generate a private key file as follows
```
In the Firebase console, open Settings > Service Accounts.

Click Generate New Private Key, then confirm by clicking Generate Key.
```
This will create a _privatekey.json_ file which will be used later.
