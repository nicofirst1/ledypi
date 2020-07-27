import math
import sys

from opensimplex import OpenSimplex

from patterns.default import Default
from utils.color import scale


class Perlin(Default):
    """
    Use perlin noise together with rgb mapping
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.pattern_name = "Perlin"
        self.x_div = 2 ** 4  # horizontal divisor
        self.y_div = 2 ** 4  # vertical divisor

        self.op = OpenSimplex()
        self.counter = 0

        self.modifiers = dict(
            x_div=self.x_div,
            y_div=self.y_div,
        )

    @property
    def y_div(self):
        return self._y_div

    @y_div.setter
    def y_div(self, value):
        self._y_div = self.strip_length // value

    def fill(self):

        # reset counter
        if self.counter == sys.maxsize - 1:
            self.counter = 0

        # color
        for idx in range(self.strip_length):
            val = self.op.noise2d(idx / self.x_div, self.counter / self.y_div)
            val = scale(val, 0, 3, -1, 1)
            self.pixels[idx]['color'] = num_to_rgb(val) + (self.color.a,)

        # update counter
        self.counter += 1


def num_to_rgb(val, max_val=3):
    i = (val * 255 / max_val)
    r = round(math.sin(0.024 * i + 0) * 127 + 128)
    g = round(math.sin(0.024 * i + 2) * 127 + 128)
    b = round(math.sin(0.024 * i + 4) * 127 + 128)
    return (r, g, b)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    noise = []
    op = OpenSimplex(seed=1)
    for idx in range(256):
        noise.append([op.noise2d(jdx / 8, idx / 8) for jdx in range(256)])

    plt.imshow(noise, cmap='gray', interpolation='lanczos')
    plt.colorbar()

    plt.show()
