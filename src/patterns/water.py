import sys

from opensimplex import OpenSimplex

from patterns.default import Default
from rgb import RGB
from utils.color import bound_add, scale


class Water(Default):
    """
    Use perlin noise with blue mapping to simulate water
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.pattern_name = "Water"

        self.x_div = 2 ** 4  # horizontal divisor
        self.y_div = 2 ** 4  # vertical divisor
        self.deepness = 100  # measure of blueness (the more the more blue)

        self.op = OpenSimplex()
        self.counter = 0

        self.counter = 0

        self.modifiers = dict(
            x_div=self.x_div,
            y_div=self.y_div,
            deepness=self.deepness,
        )

    @property
    def y_div(self):
        return self._y_div

    @y_div.setter
    def y_div(self, value):
        if value == 0: value = 0.001
        self._y_div = value

    @property
    def x_div(self):
        return self._x_div

    @x_div.setter
    def x_div(self, value):
        if value == 0: value = 0.001
        self._x_div = value

    def fill(self):

        # reset counter
        if self.counter == sys.maxsize - 1:
            self.counter = 0

        # color
        for idx in range(self.strip_length):
            val = self.op.noise2d(idx / self.x_div, self.counter / self.y_div)
            val = scale(val, 0, 255, -1, 1)

            # add base value + deepness
            val = bound_add(val, self.deepness)
            self.pixels[idx]['color'] = RGB(b=val, g=255 - val, a=self.color.a)

        # update counter
        self.counter += 1
