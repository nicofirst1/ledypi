import numpy as np

from patterns.default import Default
from rgb import RGB
from utils.color import bound_add
from utils.perlin_noise import generate_perlin_noise_2d


class Water(Default):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.increasing = False
        self.pattern_name = "Water"

        self.x_div = 2 ** 4  # horizontal divisor
        self.y_div = self.strip_length // 15  # vertical divisor
        self.deepness = 20  # measure of blueness (the less the more blue)

        self.max = 2 ** 10  ## height of the noise image, will be diplayed on the time axis
        self.base_b = 20  # min value for the blue

        # generate and normalize noise in range 0-255
        noise = generate_perlin_noise_2d((self.max, self.strip_length), (self.x_div, self.y_div))
        self.noise = (noise + 1) * 255 / 2
        self.noise = self.noise.astype(np.int)

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
        self._y_div = self.strip_length // value

    def fill(self):

        # reset counter
        if self.counter == self.max:
            self.counter = 0

        # get a slice from the noise image
        slice = self.noise[self.counter, :]

        # color
        for idx in range(self.strip_length):
            val = slice[idx] \
                # add base value + deepness
            val = bound_add(val, 255 // self.deepness + self.base_b)
            self.pixels[idx]['color'] = RGB(b=val, g=255 - val, a=self.color.a)

        # update counter
        self.counter += 1
