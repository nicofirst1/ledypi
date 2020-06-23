import math
from copy import deepcopy
from random import randint

from utils import bound_add


class RGB:
    """
    Class for rgb colors
    """

    def __init__(self, **kwargs):
        """
        Most free init ever
        :param kwargs:
        #################
        'r': red value
        'g': green value
        'b': blue value
        'c': intensity value

        If one of the above is missing then it will be set to zero, e.g. RGB() is black.
        Other setting can override
        #################

        'rgb': given another RGB class, the values will be copied
        Overrides previous inits

        #################
        'random": generate random color
        Overrides previous inits

         #################
        'white": set all values to 255
        Overrides previous inits

        """

        if "r" in kwargs.keys():
            self.assertion(kwargs["r"])
            self.r = kwargs["r"]
        else:
            self.r = 0

        if "g" in kwargs.keys():
            self.assertion(kwargs["g"])
            self.g = kwargs["g"]
        else:
            self.g = 0
        if "b" in kwargs.keys():
            self.assertion(kwargs["b"])
            self.b = kwargs["b"]
        else:
            self.b = 0

        if "c" in kwargs.keys():
            self.assertion(kwargs["c"])
            self.c = kwargs["c"]
        else:
            self.c = 0

        if "rgb" in kwargs.keys():
            self.assertion(kwargs["rgb"].r)
            self.assertion(kwargs["rgb"].g)
            self.assertion(kwargs["rgb"].b)
            self.r = kwargs["rgb"].r
            self.g = kwargs["rgb"].g
            self.b = kwargs["rgb"].b
            self.c = kwargs["rgb"].c

        if "random" in kwargs.keys():
            self.r = randint(0, 255)
            self.g = randint(0, 255)
            self.b = randint(0, 255)
            self.c = 255

        if 'white' in kwargs.keys():
            self.r = 255
            self.g = 255
            self.b = 255
            self.c = 255

    def fade(self, fade_val, minimum=10):
        """
        Fade colors
        :param fade_val: 0 to 255
        :param minimum: threshold after which
        :return:
        """

        self.r -= self.r * fade_val / 256
        self.g -= self.g * fade_val / 256
        self.b -= self.b * fade_val / 256

        self.r = math.floor(self.r)
        self.g = math.floor(self.g)
        self.b = math.floor(self.b)

        if self.r <= minimum:
            self.r = 0

        if self.g <= minimum:
            self.g = 0

        if self.b <= minimum:
            self.b = 0

    def is_black(self):

        if self.c > 0:
            if self.r > 0 or self.g > 0 or self.b > 0:
                return False

        return True

    def copy(self):
        return deepcopy(self)

    def update_single(self, **kwargs):
        """
        Update values separately
        :param kwargs: can be [r,g,b,c]
        :return:
        """

        for k, v in kwargs.items():
            self.assertion(v)
            if k == "r":
                self.r = v
            elif k == "b":
                self.b = v
            elif k == "g":
                self.g = v
            elif k == "c":
                self.c = v

    def update_color(self, color):
        self.r = color.r
        self.g = color.g
        self.b = color.b
        self.c = color.c

    def same_color(self, rgb2):
        if self.r == rgb2.r and self.g == rgb2.g and self.b == rgb2.b:
            return True

        return False

    def add_values(self, r, g, b, c):
        self.assertion(r)
        self.assertion(g)
        self.assertion(b)
        self.assertion(c)

        self.r = bound_add(self.r, r)
        self.g = bound_add(self.g, g)
        self.b = bound_add(self.b, b)
        self.c = bound_add(self.c, c)

    def add_colors(self, rgb):

        self.r = bound_add(self.r, rgb.r)
        self.g = bound_add(self.g, rgb.g)
        self.b = bound_add(self.b, rgb.b)
        # self.c = bound_add(self.c, rgb.c)

    def is_gray(self):
        if self.r == self.g == self.b:
            return True

        return False

    @staticmethod
    def assertion(val):
        assert val <= 255 and val >= 0
