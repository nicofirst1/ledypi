This dir contains shell scripts.


### Sync

The [sync](/scripts/sync.sh) script can be used to sync the ledypi repo to your raspberrypi given the correct ip address.

### Start_ledypi
The [start_ledypi](/scripts/start_ledypi.sh) can be used to start the LedyPi app on boot on the raspberry.

To do so follow this instructions:
-  `cd ledypi/scripts`
-  `sudo cp start_ledypi.sh /etc/init.d/`
-  `sudo chmod 755 /etc/init.d/start_ledypi.sh`

Test with:
- `sudo /etc/init.d/start_ledypi.sh start `
- `sudo /etc/init.d/start_ledypi.sh stop `

If it works set it to start on boot with:
- `sudo update-rc.d start_ledypi.sh defaults`

Remember to modify the parameter into the [start_ledypi](/scripts/start_ledypi.sh) to fit your needs.