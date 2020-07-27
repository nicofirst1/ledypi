from random import randint

from patterns.default import Default


class Meteor(Default):
    """
    Lights a cluster of pixels moving forward with a trail
        size: the size of the meteor
        trail_decay: the max size of the decay
        random_decay: if to use random or steady decay
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.size = 10
        self.trail_decay = 64
        self.random_decay = True
        self.step = 0
        self.pattern_name = "Meteor"

        self.modifiers = dict(
            size=self.size,
            trail_decay=self.trail_decay,
            random_decay=self.random_decay
        )

    def bound_attrs(self):
        self.size = min(self.size, self.strip_length)

    def fill(self):

        for jdx in range(self.strip_length):
            if not self.random_decay or randint(0, 10) > 5:
                self.pixels[jdx]['color'].fade(self.trail_decay)

        for jdx in range(0, self.size):
            if self.step - jdx < self.strip_length and self.step - jdx >= 0:
                self.pixels[self.step - jdx]['color'] = self.color.copy()

        self.step += 1
        self.step %= self.strip_length
