import math
from random import randint

import numpy as np

from utils.color import bound_add


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
        'a': intensity value

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

        self.rgb_vec = np.array([0, 0, 0])

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

        if "a" in kwargs.keys():
            self.assertion(kwargs["a"])
            self.a = kwargs["a"]
        else:
            self.a = 0

        if "rgb" in kwargs.keys():
            self.assertion(kwargs["rgb"].r)
            self.assertion(kwargs["rgb"].g)
            self.assertion(kwargs["rgb"].b)
            self.r = kwargs["rgb"].r
            self.g = kwargs["rgb"].g
            self.b = kwargs["rgb"].b
            self.a = kwargs["rgb"].a

        if "random" in kwargs.keys() and kwargs['random']:
            self.r = randint(0, 255)
            self.g = randint(0, 255)
            self.b = randint(0, 255)
            self.a = 255

        if 'white' in kwargs.keys():
            self.r = 255
            self.g = 255
            self.b = 255
            self.a = 255

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, value):
        self.rgb_vec[0] = value
        self._r = value

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, value):
        self.rgb_vec[1] = value
        self._g = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        self.rgb_vec[2] = value
        self._b = value

    def blend(self, other_rgb):

        alpha = 255 - ((255 - self.a) * (255 - other_rgb.a) / 255)
        red = (self.r * (255 - other_rgb.a) + other_rgb.r * other_rgb.a) / 255
        green = (self.g * (255 - other_rgb.a) + other_rgb.g * other_rgb.a) / 255
        blue = (self.b * (255 - other_rgb.a) + other_rgb.b * other_rgb.a) / 255

        self.a = int(alpha)
        self.r = int(red)
        self.g = int(green)
        self.b = int(blue)

    def scale(self):
        return np.multiply(self.rgb_vec, self.a / 255, casting='unsafe').astype(int)

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

        return self

    def is_black(self):

        if self.a > 0:
            if self.r > 0 or self.g > 0 or self.b > 0:
                return False

        return True

    def update_single(self, **kwargs):
        """
        Update values separately
        :param kwargs: can be [r,g,b,a]
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
            elif k == "a":
                self.a = v

    def update_color(self, color):
        self.r = color.r
        self.g = color.g
        self.b = color.b
        self.a = color.a

    def same_color(self, rgb2):
        if self.r == rgb2.r and self.g == rgb2.g and self.b == rgb2.b:
            return True

        return False

    def add_values(self, r, g, b, a):
        self.assertion(r)
        self.assertion(g)
        self.assertion(b)
        self.assertion(a)

        self.r = bound_add(self.r, r)
        self.g = bound_add(self.g, g)
        self.b = bound_add(self.b, b)
        self.a = bound_add(self.a, a)

    def add_colors(self, rgb):

        self.r = bound_add(self.r, rgb.r)
        self.g = bound_add(self.g, rgb.g)
        self.b = bound_add(self.b, rgb.b)

    def is_gray(self):
        if self.r == self.g == self.b:
            return True

        return False

    def copy(self):
        """
        Return a copy of self
        :return:
        """
        return RGB(r=self.r, g=self.g, b=self.b, a=self.a)

    @staticmethod
    def assertion(val):
        assert 255 >= val >= 0
