In this file you'll find all the instructions to build your controllable ledstrip.

## Requirements
- A [RaspberryPI](https://www.raspberrypi.org/products/), I'm using a  [RaspberryPi 4 Model B](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) with 4GB ram.
- A [WS2812B rgb led strip](https://www.amazon.com/BTF-LIGHTING-Flexible-Individually-Addressable-Non-waterproof/dp/B01CDTEJBG/ref=sr_1_5?dchild=1&keywords=WS2812B&qid=1596873360&sr=8-5).
 Technically you can use whatever strip (12V or 5V) as long as you provide the correct power supply and connection to the raspberry.  You can check [this out](http://www.thesmarthomehookup.com/the-complete-guide-to-selecting-individually-addressable-led-strips/) 
 for a comparison between different led strips.
 - A [5v power supply unit](https://www.amazon.com/SHNITPWR-Converter-Adapter-Transformer-WS2812B/dp/B07TZNMD8K/ref=sr_1_4?crid=11R9A0XFBC2DY&dchild=1&keywords=5v+20a&qid=1596873532&sprefix=5v+%2Caps%2C262&sr=8-4). 
 The linked one has 20 ampere for a total of `5*20=100W`. Depending on the number of leds on your strip you'll have different power needs, 
 specifically the type of led mounted on the Ws2812b draws `60 ma` per led. So for a 300 led strip you'll need at least 
 `60*300= 18000ma= 18a`
 - Some [jumper wires](https://www.amazon.com/EDGELEC-Breadboard-Optional-Assorted-Multicolored/dp/B07GD2BWPY/ref=sr_1_3?dchild=1&keywords=jumper+wires&qid=1596873841&sr=8-3) to connect the raspberryPi to the led strip (you actually need only two).
 - Electric wires
 - An internet connection 
 
## Raspberry Setup
There are plenty on excellent tutorial on how to setup a new RapsberryPi:
- [The official one](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up)
- [Using LAN](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)
 
To set a wifi connection and enable ssh protocol follow [this](https://desertbot.io/blog/headless-raspberry-pi-4-ssh-wifi-setup).

### Update
- Use ssh to log into your raspberryPi:
```shell script
ssh pi@YourPiIP
```
- (Optional) set password-less access following [this](https://linuxize.com/post/how-to-setup-passwordless-ssh-login/)

- Update with:
```shell script
sudo apt-get update && sudo apt-get -y upgrade
```

- Reboot:
```shell script
sudo reboot
```


### Python
My current raspberryPi comes with python2.7 by default and python3.7, you can check yours with 
```shell script
python --version 
> Python 2.7
ls /usr/bin/python*
```

To set python3 as default use the following:
```shell script
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2
sudo update-alternatives --config python
```

Now the version command should return something like this:
```shell script
python --version 
> Python 3.7.3
```

## Cable Connections

### Power source
Connect the power source cables to your home electric system.
This part vary depending on how you would like to connect it, just remember to keep the black with the black (minus) and the red with the red (plus)

### Raspberry
Since there is no connection powering the RaspberryPi, an usb type c power supply is necessary.

For the connection you can follow [this tutorial](https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/)  which uses following diagram:
![diagram](../Resources/diagram.png)

Where the extern power source is given by your power supply unit.
