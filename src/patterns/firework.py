import logging
from copy import copy
from random import random

from patterns.default import Default
from utils.modifier import Modifier
from utils.rgb import RGB

pattern_logger = logging.getLogger("pattern_logger")


class FireWork(Default):
    """
    Custom Game
    """

    def __init__(self, **kwargs):

        kwargs['color'] = RGB()

        super().__init__(**kwargs)

        self.pattern_name = "FireWork"
        self.increment = Modifier('fire power', 10.0, minimum=0.001, maximum=0.25)
        self.spark = Modifier('sparks', 10.0, minimum=0, maximum=1 / self.strip_length)

        for idx in range(self.strip_length):
            self.pixels[idx]['timestep'] = 0

        self.centers = []

        self.modifiers = dict(
            increment=self.increment,
            spark=self.spark,
        )

    def fill(self):

        new_pixels = copy(self.pixels)

        # increase tails for every center
        for idx in range(len(self.centers)):
            cntr, stop = self.centers[idx]

            ### back motion
            prev_pixel = new_pixels[(cntr - stop + 1) % self.strip_length]
            cur_pixel = new_pixels[(cntr - stop) % self.strip_length]

            color, timestep = drop([prev_pixel, cur_pixel], self.increment())
            ts = max(timestep - self.increment(), 0.0)
            cur_pixel['timestep'] = ts
            cur_pixel['color'] = color
            new_pixels[(cntr - stop) % self.strip_length] = cur_pixel

            ### forward motion
            prev_pixel = new_pixels[(cntr + stop - 1) % self.strip_length]
            cur_pixel = new_pixels[(cntr + stop) % self.strip_length]

            color, timestep = drop([prev_pixel, cur_pixel], self.increment())
            ts = max(timestep - self.increment(), 0.0)
            cur_pixel['timestep'] = ts
            cur_pixel['color'] = color
            new_pixels[(cntr + stop) % self.strip_length] = cur_pixel

            # increment stop for next iteration
            self.centers[idx] = (cntr, stop + 1)

        # remove all centers with a maximum stop
        self.centers = [elem for elem in self.centers if elem[1] < 1 // self.increment()]

        # fade all leds
        for idx in range(self.strip_length):
            new_pixels[idx]['color'].fade(self.increment())

        # either update pixels or spark
        for idx in range(self.strip_length):
            if random() < self.spark():
                c = RGB(random=True)
                self.pixels[idx]['color'] = c
                self.pixels[idx]['timestep'] = 1.0
                self.centers.append((idx, 1))

            else:
                self.pixels[idx]['color'] = new_pixels[idx]['color']
                self.pixels[idx]['timestep'] = new_pixels[idx]['timestep']


def drop(pixels, inc):
    """
    Perform an average on a list of pixels
    :param pixels: list[dict], list of pixels with 'color' and 'timestep' keys
    :param inc: float, increment
    :return: tuple[RGB,int]: color, timestep
    """
    tots = [elem['timestep'] for elem in pixels if not elem['color'].is_black()]

    tot = sum(tots)
    if tot == 0: tot = 0.000001

    # perform weighed average for rgba
    red = [elem['color'].r * elem['timestep'] for elem in pixels]
    red = sum(red) / tot

    green = [elem['color'].g * elem['timestep'] for elem in pixels]
    green = sum(green) / tot

    blue = [elem['color'].b * elem['timestep'] for elem in pixels]
    blue = sum(blue) / tot

    alpha = [elem['color'].a * elem['timestep'] for elem in pixels]
    alpha = sum(alpha) / tot

    # bound max and min
    red = max(red, 0)
    green = max(green, 0)
    blue = max(blue, 0)
    alpha = max(alpha, 0)

    red = min(red, 255)
    green = min(green, 255)
    blue = min(blue, 255)
    alpha = min(alpha, 255)

    # if there are no tots, use zero as average timestep
    try:
        ts = max(tots)
    except ValueError:
        ts = 0

    return RGB(r=red, g=green, b=blue, a=alpha).fade(inc), ts
