import argparse

from DotStar_Emulator.emulator.widgets.color_value import ColorValueWidget
from DotStar_Emulator.emulator.widgets.dotgrid import DotGridWidget

from Fillers.RandomFading import RandomFading
from Fillers.Snow import Snow
from Fillers.Rainbow import Rainbow
from Fillers.FireWork import FireWork
from Fillers.Steady import Steady

rate=10
color=Steady(rate)
color.run()
