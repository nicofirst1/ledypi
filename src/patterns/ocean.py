import sys

from opensimplex import OpenSimplex

from patterns.default import Default
from utils.rgb import RGB
from utils.color import bound_add, scale
from utils.modifier import Modifier


class Ocean(Default):
    """
    Use perlin noise with blue mapping to simulate water
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.pattern_name = "Ocean"

        self.x_div = Modifier('horizontal', 2 ** 4, minimum=1, maximum=2 ** 10)
        self.y_div = Modifier('vertical', 2 ** 4, minimum=1, maximum=2 ** 10)
        # measure of blueness (the more the more blue)
        self.deepness = Modifier('deepness', 10, minimum=1, maximum=255)
        self.op = OpenSimplex()
        self.counter = 0

        self.counter = 0

        self.modifiers = dict(
            x_div=self.x_div,
            y_div=self.y_div,
            deepness=self.deepness,
        )

    def fill(self):

        # reset counter
        if self.counter == sys.maxsize - 1:
            self.counter = 0

        # color
        for idx in range(self.strip_length):
            val = self.op.noise2d(idx / self.x_div(), self.counter / self.y_div())
            val = scale(val, 0, 255, -1, 1)

            # add base value + deepness
            val = bound_add(val, self.deepness())
            self.pixels[idx]['color'] = RGB(b=val, g=255 - val, a=self.color.a)

        # update counter
        self.counter += 1
