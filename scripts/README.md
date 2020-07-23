This dir contains shell scripts.


### Sync

The [sync](/scripts/sync.sh) script can be used to sync the ledypi repo to your raspberrypi given the correct ip address.

You can specify where in the rpi the directory should be synced and you __must__ input the current ledypi path as:
```shell script
bash sync.sh \path\to\ledypi
```

### Start ledypi
The [app](/scripts/app.sh) can be used to start the LedyPi app on boot on the raspberry.

To do so follow this instructions:
-  `cd ledypi/scripts`
-  `sudo cp app.sh /etc/init.d/`
-  `sudo chmod 755 /etc/init.d/app.sh`

Test with:
- `sudo /etc/init.d/app.sh start `
- `sudo /etc/init.d/app.sh stop `

If it works set it to start on boot with:
- `sudo update-rc.d ledypi.sh defaults`

Remember to modify the parameter into the [app](/scripts/app.sh) to fit your needs.

#### Running tests
If you wish to run some scripts on the rpi you should source the app with:
```shell script
source scripts/app.sh
``` 
And then execute the scripts with:
```shell script
sudo PYTHONPATH="$pythonpath" python3 your_script.py
```

#### Update
Now the scripts supports argument propagation, that is you can pass any kind of argument to the bash script which will
 then be passed to the connect script (check the [REAMDE](src/firebase/README.md)).