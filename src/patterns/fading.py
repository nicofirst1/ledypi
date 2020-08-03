from copy import deepcopy
from random import randint

from patterns.default import Default
from rgb import RGB
from utils.color import bound_sub, bound_add
from utils.modifier import Modifier


class Fading(Default):
    """
    Lights up multiple pixels with random color.
    The parameters are:
        point_number: number of maximum colored point at the same time
        rate_start: delay to light up completely a pixel
        rate_end: delay to shut offcompletely a pixel
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.point_number = Modifier('points', 30, minimum=1, maximum=self.strip_length)
        self.rate_start = Modifier('start rate', 40, minimum=1, maximum=101)
        self.rate_end = Modifier('end rate', 4, minimum=1, maximum=101)

        # assert there are no more points than leds
        self.centers = {randint(0, self.strip_length - 1): self.empty_center() for _ in range(self.point_number())}
        self.pattern_name = "Fading"

        self.modifiers = dict(
            point_number=self.point_number,
            rate_start=self.rate_start,
            rate_end=self.rate_end
        )

    def empty_center(self):
        """
        Return an empty center point as a dict with fields
        :return:
        """

        if self.randomize_color:
            default_dict = dict(color=RGB(random=True), alpha=0, delay=randint(0, 100), increasing=True)
        else:
            default_dict = dict(color=RGB(rgb=self.color), alpha=0, delay=randint(0, 100), increasing=True)

        # if there is no start in delay then alpha is maximum
        if not self.rate_start:
            default_dict['alpha'] = 255

        return default_dict

    def fill(self):

        # copy original dict
        center_copy = deepcopy(self.centers)

        # bound the rnadom point to the maximum 
        self.point_number.value = min(self.point_number(), self.strip_length)

        # for every center in the list
        for a, attr in center_copy.items():

            # get attributes
            color = attr["color"]
            alpha = attr['alpha']
            delay = attr['delay']
            increasing = attr['increasing']
            done = False

            # if point has to wait more then wait
            if delay > 0:
                self.centers[a]['delay'] -= 1
                continue

            # if increasing and there is still room for increasing do it
            if 0 <= alpha < 255 and increasing:
                alpha = bound_add(alpha, self.rate_start.max-self.rate_start(), maximum=255)
            # if not increasing and still in good range, decrease
            elif 0 < alpha <= 255 and not increasing:
                alpha = bound_sub(alpha, self.rate_end.max-self.rate_end(), minimum=0)
            # if zero and decreasing we're done
            elif alpha == 0 and not increasing:
                done = True
            # if 255 and increasing then start decreasing
            elif alpha == 255 and increasing:
                increasing = False

            # update and set color
            color.update_single(a=alpha)
            self.pixels[a]['color'] = color

            # update for original dict too
            self.centers[a]['alpha'] = alpha
            self.centers[a]['increasing'] = increasing

            # if is done
            if done:
                # pop center
                self.centers.pop(a)

                # if centers are less than supposed, add other
                if len(self.centers) < self.point_number():
                    # get a new one
                    new_c = randint(0, self.strip_length - 1)
                    while new_c in self.centers.keys():
                        new_c = randint(0, self.strip_length - 1)
                    # add it to list
                    self.centers[new_c] = self.empty_center()
