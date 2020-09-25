#!/bin/bash

path2repo="$(realpath "$0")"
path2repo="$(dirname "$path2repo")"

source $path2repo/vars.sh

function setup() {
  # installing Apache and mod_wsgi
  sudo apt-get update
  sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3

  apache_path="$path2repo/ledyweb/Apache"

  # replacing paths in Apache files
  sed -i "s|PYTHONPATH|${pythonpath}|g" "$apache_path/000-default.conf"
  sed -i "s|PYTHONHOME|${venv_path}|g" "$apache_path/000-default.conf"
  sed -i "s|LEDYPIPATH|${path2repo}|g" "$apache_path/000-default.conf"

  sudo cp "$apache_path/000-default.conf" "/etc/apache2/sites-enabled/000-default.conf"
  sudo cp "$apache_path/apache2.conf" "/etc/apache2/apache2.conf"

}


# Carry out specific functions when asked to by the system
case "$1" in
setup)
  echo "Setting up apache config files"
  setup
  ;;
start)
  echo "Starting apache web server"
  sudo apachectl restart

  ;;
chmod)
  # fix the permissions for the folder
  chgrp -R www-data $path2repo
  chmod -R 750 $path2repo
  chmod g+sw $path2repo
  ;;
*)
  echo "Usage: app {start|stop|chmod}"
  ;;
esac
