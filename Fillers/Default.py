from copy import deepcopy
from random import randint

from DotStar_Emulator.emulator.send_test_data import App

from RGB import RGB
from utils import bound_sub, circular_step


class Default(App):
    data_type = ""

    def __init__(self, args):
        """
        Init for snow effect
        :param args:
        """
        super().__init__(args)

        self.strip_length = self.grid_size.x + self.grid_size.y - 1


    def color_set(self, index, rgb, **kwargs):

        super().set(index, rgb.c, rgb.r, rgb.b, rgb.b)

    def fill(self):

       raise NotImplementedError


    def on_loop(self):
        self.fill()
        self.send()
