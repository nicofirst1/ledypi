import argparse
from random import randint

from DotStar_Emulator.emulator.widgets.color_value import ColorValueWidget
from DotStar_Emulator.emulator.widgets.dotgrid import DotGridWidget

from Fillers.ColorWipe import ColorWipe
from Fillers.Fading import Fading
from Fillers.Strobe import Strobe
from RGB import RGB

rate=100
color=RGB(white=True)
color=ColorWipe(rate,color=color)
color.run()
