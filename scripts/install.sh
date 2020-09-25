#!/bin/bash

# updates
sudo apt-get update
sudo apt-get upgrade
sudo pip3 install --upgrade setuptools

# python3
echo " installing python3"
sudo apt-get install python3-numpy python3 git python3-pip

# downloading and installing venv
echo "Building virtualenv..."
wget 'https://pypi.python.org/packages/5c/79/5dae7494b9f5ed061cff9a8ab8d6e1f02db352f3facf907d9eb614fb80e9/virtualenv-15.0.2.tar.gz'
tar -xzf virtualenv-15.0.2.tar.gz
python3 virtualenv-15.0.2/virtualenv.py --no-site-packages venv

#blinka
sudo update-alternatives --install /usr/bin/python python $(which python2) 1
sudo update-alternatives --install /usr/bin/python python $(which python3) 2
sudo update-alternatives --config python

echo " Enable I2C and SPI following the tutorial"
echo "https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi#enable-i2c-and-spi-2993390-7"

#numpy
sudo apt-get install python3-numpy


#PIllow
echo "Installing Pillow"
sudo apt-get install libjpeg-dev zlib1g-dev libfreetype6-dev liblcms1-dev libopenjp2-7 libtiff5
sudo pip3 install pillow

# installing requirements
./venv/bin/pip install -r requirements_pi.txt
