#!/bin/bash

pi_ip=192.168.178.53 # the ip of your rpi
repo_location="" # Where to sync in the rpi

files=(.git __pycache__ .idea)
excludes=()
for f in "${files[@]}"; do
  excludes+=(--exclude "$f")
done

rsync --progress -av "${excludes[@]}" -r $1 pi@$pi_ip:$repo_location
