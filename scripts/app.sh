#!/bin/sh

path2repo="/home/pi/ledypi" # change this to the location of the repo
pixels=600                  # change here the number of pixels

pythonpath="$path2repo/src:$path2repo/audio-reactive-led-strip/python"
export PYTHONPATH="$pythonpath"
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
  echo "Usage: app {start|stop}"
  ;;
esac
