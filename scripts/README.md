This dir contains shell scripts.


## Start ledypi

First you should set the number of leds in the [app](/scripts/app.sh). Then you can start the app with:

```shell script
bash scripts/app.sh start
```

And stop it with:

```shell script
bash scripts/app.sh stop
```

### On Boot

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

### Running tests
If you wish to run some scripts on the rpi you should source the app with:
```shell script
source scripts/vars.sh
``` 
And then execute the scripts with:
```shell script
sudo PYTHONPATH="$pythonpath" python3 your_script.py
```

#### Update
Now the scripts supports argument propagation, that is you can pass any kind of argument to the bash script which will
 then be passed to the connect script (check the [REAMDE](../src/firebase/README.md)).
 
 
## Sync
 
 The [sync](/scripts/sync.sh) script can be used to sync the ledypi repo from your pc to your raspberrypi given the correct ip address.
 
 First set the rpi IP-address in the _pi_ip_ variable. Then you can execute it with
 ```shell script
 bash sync.sh \PC\path\to\ledypiRepo \RPI\path\to\ledypiRepo 
 ```
If you wish to log without password follow [this](https://serverfault.com/questions/241588/how-to-automate-ssh-login-with-password):
```shell script
ssh-keygen -t rsa -b 2048
ssh-copy-id id@server
```

## Setup Apache
If you wish to use apache server to run the ledyweb app simply run 
```shell script
bash scripts/apache.sh setup
```
The script will replace the value in [000-default.conf](../ledyweb/Apache/000-default.conf) with your rpi paths, 
copy them into the [apache config folder](/etc/apache2/0) and restart apache.

You can then start it with 
```shell script
bash scripts/apache.sh start
```

If you run into permission problem try:
```shell script
bash scripts/apache.sh chmod
```

If that doesn't work you may need to add group permission to your home folder (if you are storing the repo in there) with:
```shell script
chgrp www-data $HOME
```
If the latter doesn't work either check [this out](https://serverfault.com/questions/357108/what-permissions-should-my-website-files-folders-have-on-a-linux-webserver)