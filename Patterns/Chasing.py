from random import randint

from Patterns.Default import Default
from RGB import RGB
from utils import bound_add, bound_sub


class Chasing(Default):
    data_type = "Chasing"

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.size = 1
        self.trail_decay = 64
        self.random_decay = True
        self.step = 0
        self.increasing = True
        self.second_color = RGB(random=True)

    def fill(self):

        for jdx in range(self.strip_length):
            if not self.random_decay or randint(0, 10) > 5:
                self.pixels[jdx]['color'].fade(self.trail_decay)

        for jdx in range(0, self.size):
            if self.step - jdx < self.strip_length and self.step - jdx >= 0:
                self.pixels[self.step - jdx]['color'] = self.second_color.copy()

        if 0 <= self.step < self.strip_length and self.increasing:
            self.step = bound_add(self.step, 1, maximum=255)
        elif 0 < self.step <= self.strip_length and not self.increasing:
            self.step = bound_sub(self.step, 1, minimum=0)
        else:
            self.increasing = not self.increasing

            if self.randomize_color:

                self.second_color = RGB(random=True)

            else:
                self.second_color = self.color
