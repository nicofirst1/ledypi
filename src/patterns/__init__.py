import logging
import sys

from patterns.color_wipe import ColorWipe
from patterns.equation import Equation
from patterns.fading import Fading
from patterns.fire import Fire
from patterns.firework import FireWork
from patterns.game_of_life import GameOfLife
from patterns.image import Image
from patterns.meteor import Meteor
from patterns.music import Music
from patterns.off import Off
from patterns.perlin import Perlin
from patterns.pulse import Pulse
from patterns.rainbow import Rainbow
from patterns.snow import Snow
from patterns.steady import Steady
from patterns.storm import Storm
from patterns.water import Water

pattern_logger = logging.getLogger("pattern_logger")
pattern_logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s\n')
handler.setFormatter(formatter)
pattern_logger.addHandler(handler)

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
    Water=Water,
    Perlin=Perlin,
    GameOfLife=GameOfLife,
    Image=Image,
    Storm=Storm,
)
