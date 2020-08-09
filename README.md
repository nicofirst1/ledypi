<h1 align="center">
  <br>
    <img src="Resources/logo.png"  width="250"></a>
  <br>
  Ledypi
</h1>

<h4 align="center">Control you led strip with  RaspberryPi, Python and Android</a>.</h4>

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://forthebadge.com/images/badges/made-with-python.svg"
         a>
  </a>
  <a href="https://forthebadge.com/images/badges/built-with-love.svg">
      <img src="https://forthebadge.com/images/badges/built-with-love.svg">
  </a>

</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#Patterns">Patterns</a> •
  <a href="#Installation">Installation</a> •
  <a href="#Running">Running</a> •
  <a href="#Contributing">Contributing</a>
</p>

<h4 align="center">
  Click video for tutorial 
</h4>

<p align="center" 
    href="https://youtu.be/c0NvfBiJOkw">
    <img src="Resources/tutorials/ledyweb_tutorial.gif"  width="450" >
</p>


<br>
<br>


# Key Features
Choose from more than 10 pre-made patterns and implement your own.
The modular desing allows you to add the logic you wish by overriding a single method, then you can choose the pattern either trough ssh or on the android app.

- 14 pre-made patterns
- Customizable attributes for each one
- [Music reactive](#music-reactive-click-gif-for-video) 
- [Android app](AppInventor) for control 
- [LedyWeb](https://github.com/nicofirst1/ledyweb) online controller 
- Firebase database
- Debug mode available 

# Patterns
Each pattern inherits from a [base class](src/patterns/default.py) with its own logic. This allows anyone to implement his own pattern simply by overriding a method (see more on the [readme](patterns/README.md)).

Moreover each pattern can be customized by changing the values of its attributes, more ahead.

## Fixed logic
There are more than 10 _standard_ pattern to choose from with a steady logic, that is a fixed behavior.

### Water

Bring the ocean home with the ocean pattern. You can choose the deepness with the parameters

![water demo](Resources/patterns/water_demo.gif)

### Fire

If you're cold then try the fire pattern.

![water demo](Resources/patterns/fire_demo.gif)




## Interactive
On top of these fixed patters there are two interactive patters whose behavior can completely change based on the user input"

### Music Reactive (click gif for video)
[![audio demo](Resources/patterns/audio_demo.gif)](https://youtu.be/7PXDBr3uZmA) 

This pattern uses a microphone to visualize the music on your led strip. There are three different type of visualization:
- Spectrum: split the strip on subsequent frequency bands and visualize the amplitude as a mix of rgb values
- Energy: use an energy function to plot the sound on the leds
- Scroll: record the audio amplitude on a scrolling timeline.


### Image
Designing a pattern can become hard and take some time, so why not using a pre-made pattern?

With _Image_ you can use an URL pointing to an image and LedyPi will download it and display it for you.

![image demo](Resources/patterns/image_demo.gif)

## Complete List
Check out the list of available patterns [here](markdowns/PATTERNS.md)

# Installation 
For the installation check out the related [INSTALL file](markdowns/INSTALL.md).

# Running 
Once you have installed the project on the RaspberryPi you can start it with the [start script](scripts):
```shell script
bash ledypi/scripts/app.sh start
```

For the web controller run it with ( more options are available in the ledyweb [README](ledyweb/README.md)):
```shell script
python manage.py start
```

For testing see the [USAGE file](markdowns/USAGE.md)

# Contributing
If you wish to support this project just fork it and add your pattern following the [readme](src/patterns/README.md).

<a href="https://paypal.me/dizzi17">
  <img src="https://img.shields.io/badge/-donate-0079C1.svg?style=for-the-badge&logo=paypal">
</a>
&nbsp;&nbsp
<a href="https://www.linkedin.com/in/nicol%C3%B2-brandizzi-04091b153/">
  <img src="https://img.shields.io/badge/-LinkedIn-2867b2.svg?style=for-the-badge&logo=linkedin">
</a>