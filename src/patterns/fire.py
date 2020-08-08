from math import ceil
from random import randint

from patterns.default import Default
from utils.rgb import RGB
from utils.color import bound_sub
from utils.modifier import Modifier


class Fire(Default):
    """
    Fire pattern
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.cooling = Modifier('cooling', 10, minimum=1, maximum=100)
        self.sparking = Modifier('sparking', 40, minimum=1, maximum=255)
        self.cooldown_list = [0 for _ in range(self.strip_length)]
        self.pattern_name = "Fire"
        self.mid = self.strip_length // 2

        self.modifiers = dict(
            cooling=self.cooling,
            sparking=self.sparking
        )

    def bound_attrs(self):
        self.sparking.value = min(self.sparking(), 255)

    def fill(self):

        self.bound_attrs()

        # cooling_down
        for idx in range(self.strip_length):
            cooldown = randint(0, ceil(((self.cooldown_list[idx] * 10) / self.strip_length)) + self.cooling())
            self.cooldown_list[idx] = bound_sub(self.cooldown_list[idx], cooldown, minimum=0)

        for idx in range(self.strip_length - 1, self.mid, -1):
            v = (self.cooldown_list[idx - 1] + 2 * self.cooldown_list[idx - 2]) / 3
            self.cooldown_list[idx] = v

        for idx in range(0, self.mid - 1, +1):
            v = (self.cooldown_list[idx + 1] + 2 * self.cooldown_list[idx + 2]) / 3
            self.cooldown_list[idx] = v

        if randint(0, 255) < self.sparking():
            # sparking starting point
            y = randint(self.mid - 3, self.mid + 3)
            self.cooldown_list[y] = self.cooldown_list[y] + randint(160, 255)

        for idx in range(self.strip_length):
            self.pixels[idx]['color'] = heat_to_rgb(self.cooldown_list[idx])


def heat_to_rgb(temperature):
    t192 = round((temperature / 255.0) * 191)
    heatramp = t192 & 0x3F
    heatramp <<= 2

    if t192 > 0x80:
        return RGB(r=255, g=255, b=heatramp, a=255)
    elif t192 > 0x40:
        return RGB(r=255, g=heatramp, b=0, a=255)
    else:
        return RGB(r=heatramp, g=0, b=0, a=255)
