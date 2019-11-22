from math import ceil
from random import random, randint

from Fillers.Default import Default
from RGB import RGB
from utils import bound_sub


class Fire(Default):
    data_type = "Fire"

    def __init__(self, rate,cooling=60,sparking=50, speed=20):
        """
        Init for steady color
        :param args: for App
        :param trail_length: length of snow trail
        """
        super().__init__(rate)


        #assert 20<=cooling<=100
        assert 50<=sparking<=200
        assert 0<=speed<=20

        self.cooling=cooling
        self.sparking=sparking
        self.speed=speed
        self.color = RGB(random=True)
        self.alpha=255

        self.pixels=[0 for _ in range(self.strip_length)]


    def fill(self):
        # cooling_down
        for idx in range(self.strip_length):
            cooldown = randint(0, ceil(((self.cooling * 10) / self.strip_length)) + 2)
            self.pixels[idx]=bound_sub(self.pixels[idx],cooldown,minimum=0)

        for idx in range(self.strip_length - 1, 2, -1):
            self.pixels[idx] = (self.pixels[idx - 1] + self.pixels[idx - 2] + self.pixels[idx - 2]) / 3

        if randint(0,255) < self.sparking:
            y = randint(0,7)
            self.pixels[y] = self.pixels[y] + randint(160, 255)

        for idx in range(self.strip_length):
            self.color_set(idx, heat_to_rgb(self.pixels[idx]))


def heat_to_rgb(temperature):
    t192=round((temperature/255.0)*191)
    heatramp = t192 & 0x3F
    heatramp <<= 2

    if t192 > 0x80:
        return RGB(r=255,g=255,b=heatramp,c=255)
    elif  t192 > 0x40:
        return RGB(r=255,g=heatramp,b=0,c=255)
    else:
        return RGB(r=heatramp,g=0,b=0,c=255)
