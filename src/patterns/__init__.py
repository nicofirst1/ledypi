import logging
import sys

from patterns.color_wipe import ColorWipe
from patterns.fading import Fading
from patterns.fire import Fire
from patterns.firework import FireWork
from patterns.meteor import Meteor
from patterns.music import Music
from patterns.off import Off
from patterns.pulse import Pulse
from patterns.rainbow import Rainbow
from patterns.snow import Snow
from patterns.steady import Steady

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

)
