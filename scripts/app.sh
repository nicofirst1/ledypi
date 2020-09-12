#!/bin/bash

pixels=600 # change here the number of pixels

path2repo="$(realpath "$0")"
path2repo="$(dirname "$path2repo")"

source $path2repo/vars.sh

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
