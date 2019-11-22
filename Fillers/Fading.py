from copy import deepcopy
from random import randint

from DotStar_Emulator.emulator.send_test_data import App

from Fillers.Default import Default
from RGB import RGB
from utils import bound_sub, bound_add


class Fading(Default):
    data_type = "Fading"

    def __init__(self, rate, random_points=20, rate_start=40, rate_end=4, color='rand'):


        # assert delays are in range
        assert 0 <= rate_start <= 50
        assert 0 <= rate_end <= 50

        self.color=color

        super().__init__(rate)
        self.random_points = random_points
        self.rate_start = rate_start
        self.rate_end = rate_end

        # assert there are no more points than leds
        assert random_points < self.strip_length
        self.centers = {randint(0, self.strip_length - 1): self.empty_center() for _ in range(random_points)}

    def empty_center(self):
        """
        Return an empty center point as a dict with fields
        :return:
        """

        if self.color=='rand':
            default_dict = dict(color=RGB(random=True), alpha=0, delay=randint(0, 10), increasing=True)
        else:
            default_dict = dict(color=RGB(rgb=self.color), alpha=0, delay=randint(0, 10), increasing=True)

        # if there is no start in delay then alpha is maximum
        if not self.rate_start:
            default_dict['alpha'] = 255

        return default_dict


    def fill(self):

        # copy original dict
        center_copy = deepcopy(self.centers)

        # for every center in the list
        for c, attr in center_copy.items():

            # get attributes
            color = attr["color"]
            alpha = attr['alpha']
            delay = attr['delay']
            increasing = attr['increasing']
            done = False

            # if point has to wait more then wait
            if delay > 0:
                self.centers[c]['delay'] -= 1
                continue

            # if increasing and there is still room for increasing do it
            if 0 <= alpha < 255 and increasing:
                alpha = bound_add(alpha, self.rate_end, maximum=255)
            # if not increasing and still in good range, decrease
            elif 0 < alpha <= 255 and not increasing:
                alpha = bound_sub(alpha, self.rate_start, minimum=0)
            # if zero and decreasing we're done
            elif alpha == 0 and not increasing:
                done = True
            # if 255 and increasing then start decreasing
            elif alpha == 255 and increasing:
                increasing = False

            # update and set color
            color.update_single(c=alpha)
            self.color_set(c, color)

            # update for original dict too
            self.centers[c]['alpha'] = alpha
            self.centers[c]['increasing'] = increasing

            # if is done
            if done:
                # pop center
                self.centers.pop(c)
                # get a new one
                new_c = randint(0, self.strip_length - 1)
                while new_c in self.centers.keys():
                    new_c = randint(0, self.strip_length - 1)
                # add it to list
                self.centers[new_c] = self.empty_center()
