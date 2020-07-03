from patterns.chasing import Chasing
from patterns.color_wipe import ColorWipe
from patterns.fading import Fading
from patterns.fire import Fire
from patterns.firework import FireWork
from patterns.meteor import Meteor
from patterns.rainbow import Rainbow
from patterns.snow import Snow
from patterns.steady import Steady
from patterns.strobe import Strobe

import logging
import sys

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
    Rainbow=Rainbow,
    Snow=Snow,
    Steady=Steady,
    Strobe=Strobe,
    Chasing=Chasing,

)
