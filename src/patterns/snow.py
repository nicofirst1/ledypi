from copy import copy

from patterns.default import Default
from rgb import RGB
from utils.modifier import Modifier


class Snow(Default):
    """
    Define n moving clusters with a trail
        trail: the length of the trail
        min_space: the minimum space between the clusters
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.trail = Modifier('trail size', 5, minimum=1, maximum=self.strip_length//2)
        # min space between trail end and trail start
        self.min_space = Modifier('trail size', 3, minimum=1, maximum=self.strip_length // 2)
        self.counter = 0
        self.pattern_name = "Snow"
        self.color = RGB(white=True)

        self.modifiers = dict(
            trail=self.trail,
            min_space=self.min_space,
        )

    def fill(self):

        # get the number of trails the strip can have
        num_of_trail = self.strip_length // (self.trail() + self.min_space())
        # make them even
        if num_of_trail % 2 != 0:
            num_of_trail -= 1

        intensity = self.color.a
        loss = intensity // self.trail()  # loss of intensity for trail
        color = copy(self.color)

        for jdx in reversed(range(num_of_trail)):
            for idx in range(jdx + self.counter, self.strip_length + jdx + self.counter, num_of_trail):
                color.update_single(a=intensity)
                self.pixels[idx % self.strip_length]['color'] = color.copy()

            if not intensity - loss < 0:
                intensity -= loss
            else:
                intensity = 0

        self.update_counter()

    def update_counter(self):
        self.counter += 1
        self.counter %= self.strip_length
