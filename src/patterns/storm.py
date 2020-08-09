from random import random, randint

from patterns.default import Default
from utils.color import bound_sub, bound_add
from utils.modifier import Modifier
from utils.rgb import RGB


class Storm(Default):
    """
    Steady color
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pattern_name = "Storm"

        self.rain = Modifier('rain intensity', 10.0, minimum=0, maximum=0.2)
        self.thunder = Modifier('thunder intensity', 5.0, minimum=0, maximum=0.2)
        self.thunder_size = Modifier('thunder size', 80, minimum=0, maximum=self.strip_length)

        self.thunder_color = RGB(white=True)
        self.rain_color = RGB(r=70, g=100, b=255, a=255)
        self.thunder_centers = {}

        for idx in range(self.strip_length):
            self.pixels[idx]['rain'] = 0

    def fill(self):

        def rain_handler(idx):
            rn = self.pixels[idx]['rain']

            if not rn:
                rn = 255 * random() if random() < self.rain() else 0

            else:
                rn = bound_sub(rn, rain_loss)

            self.pixels[idx]['rain'] = rn

            if rn:
                c = self.rain_color.copy()
                c.blend(self.pixels[idx]['color'])
                c.update_single(a=rn)

                self.pixels[idx]['color'] = c

        def thunder_handler(idx):
            """
            Handle thunder
            :param idx:
            :return:
            """
            # if current index is a thunder center
            if idx in self.thunder_centers.keys():
                # get the values
                start, end, alpha = self.thunder_centers[idx]

                # mimic thunder behavior to brighten up with random value
                if random() < 0.1:
                    alpha = bound_add(alpha, thunder_loss * 2)
                else:
                    alpha = bound_sub(alpha, thunder_loss)

                # update alpha
                self.thunder_centers[idx][2] = alpha

                # for every part of the thunder
                for jdx in range(start, end + 1):
                    # copy the thunder color
                    c = self.thunder_color.copy()
                    # estimate the distance from center as a loss + a random term
                    l = 200 * abs(jdx - idx) / self.thunder_size() // 2 + randint(0, 50)
                    # estimate new local alpha
                    v = bound_sub(alpha, thunder_loss + l)
                    # update in color
                    c.update_single(a=v)
                    # set
                    # c.blend(self.pixels[jdx]['color'])
                    self.pixels[jdx]['color'] = c

                # if alpha is zero then remove the center
                if alpha == 0:
                    del self.thunder_centers[idx]

        thunder_loss = 30
        rain_loss = 10

        # if there are not enough thunders
        max_centers = self.strip_length // self.thunder_size()
        if len(self.thunder_centers) < max_centers and random() < self.thunder():

            # get how many more do we need
            max_centers -= len(self.thunder_centers)
            for _ in range(max_centers):
                # if probability is high enough
                # estimate random center
                center = randint(0, self.strip_length)
                size = self.thunder_size()

                # get start and end
                start = center - size // 2 - randint(0, size // 4)
                start = start if start >= 0 else 0

                end = size // 2 + center + randint(0, size // 4)
                end = end if end < self.strip_length else self.strip_length

                # add it to dictionary
                self.thunder_centers[center] = [start, end, 255]

        for i in range(self.strip_length):
            rain_handler(i)
            thunder_handler(i)
