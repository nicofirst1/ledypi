#!/bin/bash

path2repo="$( dirname $( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd ))"
echo "Your path is: $path2repo"
pixels=600                  # change here the number of pixels

pythonpath="$path2repo/src:$path2repo/audio-reactive-led-strip/src:$path2repo/ledyweb"
export PYTHONPATH="$pythonpath"
# Carry out specific functions when asked to by the system
case "$1" in
start)
  echo "Starting LedyPi with $pixels pixels"
  # run application you want to start
  sudo PYTHONPATH="$pythonpath" python3 $path2repo/src/firebase/control.py $path2repo/src/firebase/credential.json rpi --pixels $pixels "${@:2}" &
  ;;
stop)
  echo "Stopping LedyPi"
  # kill application you want to stop
  sudo pkill --signal SIGINT -f firebase/control.py -e
  ;;
*)
  echo "Usage: app {start|stop}"
  ;;
esac
