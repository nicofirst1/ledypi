from random import randint

from Fillers.Default import Default
from RGB import RGB
from utils import bound_add, bound_sub


class Chasing(Default):
    data_type = "Chasing"

    def __init__(self, delay, size=2, trail_decay=64, random_decay=True):
        """
        Init for steady color
        :param args: for App
        :param trail_length: length of snow trail
        """
        super().__init__(delay)

        self.color = RGB(random=True)
        self.size=size
        self.trail_decay=trail_decay
        self.random_decay=random_decay
        self.step=0
        self.increasing=True


    def fill(self):



        for jdx in range(self.strip_length):
            if not self.random_decay or randint(0,10) > 5:
                self.pixels[jdx]['color'].fade(self.trail_decay)

        for jdx in range( 0, self.size):
            if self.step-jdx< self.strip_length and self.step-jdx>=0:
                self.pixels[self.step-jdx]['color']=self.color.copy()

        if 0 <= self.step < self.strip_length and self.increasing:
            self.step = bound_add(self.step, 1, maximum=255)
        elif 0 < self.step <= self.strip_length and not self.increasing:
            self.step = bound_sub(self.step, 1, minimum=0)
        else:
            self.increasing=not self.increasing
            self.color=RGB(random=True)





