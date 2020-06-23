## Installation 
First install the custom DotStar_emulator. Cd into the [dir](DotStar_Emulator/), source your python env if any and execute:

`python setup.py install`.


### Firecode 

#### Creating databse

#### Linking to app inventor
Check [this out](https://rominirani.com/tutorial-mit-app-inventor-firebase-4be95051c325) to link app inventor with firebase

#### Generatig private key file
To generate a private key file for your service account:

    In the Firebase console, open Settings > Service Accounts.

    Click Generate New Private Key, then confirm by clicking Generate Key.

    Securely store the JSON file containing the key.
    




## Testig
### Local 
To test first run the [gui](main_gui.py) and then in a separate process run [patterns](test.py)
```
python main_gui.py
python patterns.py
```

### Database
To test the app together with the database you will need to have the app running on your phone and start both connection and the main gui in different processes
```
python main_gui.py
python FireBase/Connection.py
```
Once you are done you can change the patterns from the app on your phone and check the updates in real time on the screen