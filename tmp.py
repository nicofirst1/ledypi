import argparse
from random import randint

from DotStar_Emulator.emulator.widgets.color_value import ColorValueWidget
from DotStar_Emulator.emulator.widgets.dotgrid import DotGridWidget

from Fillers.ColorWipe import ColorWipe
from Fillers.Fading import Fading
from Fillers.Fire import Fire
from Fillers.FireWork import FireWork
from Fillers.Meteor import Meteor
from Fillers.Rainbow import Rainbow
from Fillers.Snow import Snow
from Fillers.Strobe import Strobe
from Fillers.Steady import Steady

from RGB import RGB

rate=10
color=RGB(white=True)
app=Rainbow(rate)
app.run()
