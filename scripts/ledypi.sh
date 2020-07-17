#!/bin/sh

path2repo="/home/pi/Repos/ledypi" # change this to the location of the repo
pixels=600                         # change here the number of pixels

# Carry out specific functions when asked to by the system
case "$1" in
start)
  echo "Starting LedyPi"
  # run application you want to start
  sudo PYTHONPATH="$path2repo/src" python3 $path2repo/src/firebase/connect.py $path2repo/src/firebase/credential.json rpi --pixels $pixels "${@:2}" &
  ;;
stop)
  echo "Stopping LedyPi"
  # kill application you want to stop
  sudo pkill --signal SIGINT -f firebase/connect.py -e
  ;;
*)
  echo "Usage: /etc/init.d/noip {start|stop}"
  exit 1
  ;;
esac
