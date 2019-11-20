import argparse

from DotStar_Emulator.emulator.widgets.color_value import ColorValueWidget
from DotStar_Emulator.emulator.widgets.dotgrid import DotGridWidget

from Fillers.RandomFading import RandomFading
from Fillers.Snow import Snow
from Fillers.Rainbow import Rainbow
from Fillers.FireWork import FireWork

args=argparse.Namespace(rate=10,loop=True)
color=RandomFading(args)
color.run()
