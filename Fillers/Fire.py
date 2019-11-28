from math import ceil
from random import random, randint

from Fillers.Default import Default
from RGB import RGB
from utils import bound_sub


class Fire(Default):
    data_type = "Fire"

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.cooling=60
        self.sparking=50
        self.alpha=255
        self.cooling=[0 for _ in range(self.strip_length)]


    def fill(self):
        # cooling_down
        for idx in range(self.strip_length):
            cooldown = randint(0, ceil(((self.cooling[idx] * 10) / self.strip_length)) + 2)
            self.cooling[idx]=bound_sub(self.cooling[idx], cooldown, minimum=0)

        for idx in range(self.strip_length - 1, 2, -1):
            self.cooling[idx] = (self.cooling[idx - 1] + self.cooling[idx - 2] + self.cooling[idx - 2]) / 3

        if randint(0,255) < self.sparking:
            y = randint(0,7)
            self.cooling[y] = self.cooling[y] + randint(160, 255)

        for idx in range(self.strip_length):
            self.pixels[idx]['color']= heat_to_rgb(self.cooling[idx])


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
