import logging
from random import random

from patterns.default import Default
from utils.modifier import Modifier
from utils.rgb import RGB

pattern_logger = logging.getLogger("pattern_logger")


class GameOfLight(Default):
    """
    Custom Game
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.pattern_name = "GameOfLight"
        self.increment = Modifier('Increment', 50.0, minimum=0, maximum=1)
        self.spark = Modifier('Spark', 10.0, minimum=0, maximum=0.5)
        self.initial_prob = Modifier('Initial prob', 50.0, minimum=0, maximum=1)

        self.modifiers = dict(
            increment=self.increment,
            spark=self.spark,
            initial_prob=self.initial_prob
        )

        self.to_init = True

    def init_colors(self):
        for idx in range(self.strip_length):
            if random() < self.initial_prob():
                self.pixels[idx]["color"] = RGB(random=True)

    def fill(self):

        # init random color if is start
        if self.to_init:
            self.init_colors()
            self.to_init = False

        new_pixels = []
        for idx in range(self.strip_length):
            # get values
            prev_color = self.pixels[(idx - 1) % self.strip_length]['color']
            cur_color = self.pixels[idx]['color']
            next_color = self.pixels[(idx + 1) % self.strip_length]['color']

            # estimate new rgb values
            r = compare_win(prev_color.r, cur_color.r, next_color.r, self.increment())
            g = compare_win(prev_color.g, cur_color.g, next_color.g, self.increment())
            b = compare_win(prev_color.b, cur_color.b, next_color.b, self.increment())

            # define next state
            new_pixels.append(RGB(r=r, g=g, b=b, a=255))

        # apply changes with a chance of random sparking
        for idx in range(self.strip_length):
            if random() < self.spark():
                self.pixels[idx]['color'] = RGB(random=True)
            else:
                self.pixels[idx]['color'] = new_pixels[idx]


def compare_win(pc, cc, nc, inc=0.1):
    """
    The middle value 'cc' depend on the two neightboors 'pc' and 'nc'.
    There are 9 possible comparison results, we'll use 'g' (greater) if cc>x, 'e' (equal) if cc==x and 'l' (lower) is cc<x.
    The cases are the following
    gxg     lxl     exe
    exg     exl     lxg
    gxe     lxe     gxl

    The first column is treated as cc wins against the neighbors so its value is reduced by cc*inc
    The second column is treated as cc looses against the neighbors so its value is increased.
    If all of them are equal increase by a random value
    If there is a lower and a greater average the value.

    :param pc: int, previous color
    :param cc: int, current color
    :param nc: int, next color
    :param inc: float, de/increment
    :return:
    """

    # first column
    if cc > pc and cc > nc:
        new_val = cc * inc
    elif pc == cc > nc:
        new_val = cc * inc
    elif nc == cc > pc:
        new_val = cc * inc

    # second column
    elif cc < pc and cc < nc:
        new_val = cc + cc * inc
    elif pc == cc < nc:
        new_val = cc + cc * inc
    elif nc == cc < pc:
        new_val = cc + cc * inc

    # equivalence
    elif nc == cc == pc:
        if cc == 0:
            new_val = 255 * random()
        else:
            new_val = cc + cc * random()

    # gxl, lxg
    else:
        new_val = (pc + nc) // 2

    if new_val > 255:
        new_val = 255
    elif new_val < 0:
        new_val = 0

    return int(new_val)
