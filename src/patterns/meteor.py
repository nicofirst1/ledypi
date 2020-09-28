from random import random

from patterns.default import Default
from utils.modifier import Modifier


class Meteor(Default):
    """
    Lights a cluster of pixels moving forward with a trail
        size: the size of the meteor
        trail_decay: the max size of the decay
        random_decay: if to use random or steady decay
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.size = Modifier('size', 5, minimum=1, maximum=self.strip_length)
        self.trail_decay = Modifier('trail decay', 5, minimum=0, maximum=1)
        self.random_decay = Modifier('random decay', True)

        self.step = 0
        self.pattern_name = "Meteor"

        self.modifiers = dict(
            size=self.size,
            trail_decay=self.trail_decay,
            random_decay=self.random_decay
        )

    def fill(self):

        for jdx in range(self.strip_length):
            if not self.random_decay() or random() > 0.5:
                px = self.pixels[jdx]['color']
                self.pixels[jdx]['color'] = px.fade(self.trail_decay(inverse=True))

        for jdx in range(0, self.size()):
            if self.step + jdx < self.strip_length and self.step - jdx >= 0:
                self.pixels[self.step - jdx]['color'] = self.color.copy()

        self.step += 1
        self.step %= self.strip_length
