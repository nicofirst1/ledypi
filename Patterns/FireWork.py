from copy import deepcopy
from random import randint

from Patterns.Default import Default
from RGB import RGB
from utils import bound_sub, circular_step


class FireWork(Default):
    data_type = "FireWork"

    def __init__(self, kwargs):

        super().__init__(**kwargs)
        self.fires = 5
        self.use_add = False
        self.loss = 25
        self.step = 0
        self.centers = {randint(0, self.strip_length - 1): self.empty_center() for _ in range(self.fires)}

    def empty_center(self):
        if self.randomize_color:
            return dict(color=RGB(random=True), tail=[], step=0)
        else:
            return dict(color=self.color, tail=[], step=0)


    def bound_attrs(self):
        self.fires=min(self.fires,self.strip_length)

    def fill(self):

        self.bound_attrs()

        loss_weight = 1.3
        center_copy = deepcopy(self.centers)

        # for every center in the list
        for c, attr in center_copy.items():

            # get the color and the tail
            color = attr["color"]
            step = attr["step"]
            has_popped = False

            # estimate the center intesity and update
            ci = bound_sub(255, loss_weight * self.loss * step)
            color.update_single(c=ci)
            self.add_update_pixel(c, color)

            idx = 1

            # if the intensity is more than zero, the the tail is still increasing
            if ci > 0:
                # for 1 to the current step
                for idx in range(idx, step + 1):
                    # get previous and next led
                    p = c - idx
                    n = c + idx
                    p %= self.strip_length
                    n %= self.strip_length

                    # estimate intensity and update
                    # ci is= 255 - the loss times the current step and the index (farther points from center are newer)
                    ci = bound_sub(255, self.loss * (loss_weight * step + 1 - idx))
                    color.update_single(c=ci)

                    self.add_update_pixel(p, color)
                    self.add_update_pixel(n, color)

                    # update tail
                    attr["tail"].append((p, n, idx))
                # remove duplicates
                attr["tail"] = list(set(attr["tail"]))

            # if the center has faded then the tails need to fade too
            else:
                # if there are some non zero tail
                if len(attr["tail"]) > 0:
                    # for every tail
                    for t in attr["tail"]:
                        # get previous, next and index
                        p = t[0]
                        n = t[1]
                        idx = t[2]
                        # estimate ci as before
                        ci = bound_sub(255, self.loss * (loss_weight * step + 1 - idx))
                        # update
                        color.update_single(c=ci)
                        self.add_update_pixel(p, color)
                        self.add_update_pixel(n, color)
                        # if ci is zero remove point from tail
                        if ci == 0:
                            attr["tail"].pop(attr["tail"].index(t))

                # if the center is faded and it has no more tail
                else:
                    # remove the center
                    self.centers.pop(c)

                    if len(self.centers)<self.fires:

                        for _ in range(self.fires-len(self.centers)):

                            # get another one which is not in the center lists already
                            rd = randint(0, self.strip_length - 1)
                            while rd in self.centers.keys():
                                rd = randint(0, self.strip_length - 1)
                            # put random color
                            self.centers[rd] = self.empty_center()
                        has_popped = True

            # is the center has been removed then dont update
            if not has_popped:
                try:
                    self.centers[c]["tail"] = attr["tail"]
                    step = circular_step(step, self.strip_length)
                    self.centers[c]["step"] = step
                except KeyError:
                    pass

        self.update_couter()

    def add_update_pixel(self, idx, new_color):

        self.pixels[idx]['color'] = new_color
        # current_color = self.pixels[idx]['color']

        # if current_color.same_color(new_color) or current_color.is_gray():
        #     self.pixels[idx]['color']=new_color
        # elif self.use_add:
        #     self.pixels[idx]['color'].add_colors(new_color)
        # else:
        #     self.pixels[idx]['color']=new_color

    def update_couter(self):
        self.step += 1
        self.step %= self.strip_length


