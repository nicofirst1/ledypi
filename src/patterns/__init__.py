from patterns.color_wipe import ColorWipe
from patterns.colormap import ColorMap
from patterns.equation import Equation
from patterns.fading import Fading
from patterns.fire import Fire
from patterns.firework import FireWork
from patterns.game_of_life import GameOfLife
from patterns.image import Image
from patterns.meteor import Meteor
from patterns.music import Music
from patterns.ocean import Ocean
from patterns.off import Off
from patterns.perlin import Perlin
from patterns.pulse import Pulse
from patterns.rainbow import Rainbow
from patterns.snow import Snow
from patterns.sorting import Sorting
from patterns.steady import Steady
from patterns.storm import Storm
from src import loggers

pattern_logger = loggers["patterns"]

Patterns = dict(
    ColorWipe=ColorWipe,
    Fading=Fading,
    Fire=Fire,
    FireWork=FireWork,
    Meteor=Meteor,
    Off=Off,
    Rainbow=Rainbow,
    Snow=Snow,
    Steady=Steady,
    Pulse=Pulse,
    Music=Music,
    Equation=Equation,
    Ocean=Ocean,
    Perlin=Perlin,
    GameOfLife=GameOfLife,
    Image=Image,
    Storm=Storm,
    Sorting=Sorting,
    ColorMap=ColorMap,
)
