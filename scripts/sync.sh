#!/bin/bash

pi_ip=192.168.178.53
repo_location="Repos/"


rsync --progress -r ../../ledypie pi@$pi_ip:$repo_location