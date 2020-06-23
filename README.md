# Setup
This project uses three main tools:
1. [DotStar_emulator](https://github.com/chrisrossx/DotStar_Emulator)
2. [AppInventor](http://appinventor.mit.edu/)
3. [Firebase](https://console.firebase.google.com/)

In the following I will guide you to the installation and setup required to make everything work

## Python 3.7
The project works with python>=3.6, to setup your environment follow the steps:
- (Optional) source your environment, 
- Install the required modules: `pip install -r requirements.txt `
- As mentioned before, this project uses a custom implementation on the [DotStar_emulator repo](https://github.com/chrisrossx/DotStar_Emulator). Installit with:
```
python DotStar_Emulator/setup.py install
```

## App Inventor
The MIT [AppInventor](http://appinventor.mit.edu/) is a tool to simply create apps with a building block programming paradigm. 
The first thing you'll need to do is make an account.
Then you can import the app from the [ledypie.aia](AppInventor/ledypie.aia) file:
```
Click on 'Create Apps!'
Login
Click on 'My Projects' on the top left 
Import project (.aia) from my computer ...
And select the ledypie.aia file
```
You can check the [README](AppInventor/README.md) in the AppInventor directory for a detailed explanation of the app.

### Firebase
The communication between the app and python is done through the [Firebase](https://console.firebase.google.com/) database.

#### Database creation and linking 
To create a Firebase database and link it to the app use [this tutorial](https://rominirani.com/tutorial-mit-app-inventor-firebase-4be95051c325).
Be aware that the FireBaseDB is already present in the app so you don't need to instantiate a new one, simply fill out the _FirebaseToken_ and _FirebaseURL_

#### Generating private key file
To connect the database with the python application you will need to generate a private key file as follows
```
In the Firebase console, open Settings > Service Accounts.

Click Generate New Private Key, then confirm by clicking Generate Key.
```
This will create a _privatekey.json_ file which will be used later.

# Testing
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