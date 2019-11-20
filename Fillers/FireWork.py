from copy import deepcopy
from random import randint

from DotStar_Emulator.emulator.send_test_data import App

from RGB import RGB
from utils import bound_sub, circular_step


class FireWork(App):
    data_type = "FireWork"

    def __init__(self, args, num_of_fires=5, usa_add=False):
        """
        Init for snow effect
        :param args:
        """
        super().__init__(args)

        self.fires = num_of_fires
        self.use_add=usa_add
        self.loss = 25
        self.strip_length = self.grid_size.x + self.grid_size.y - 1
        self.step = 0
        self.centers = {randint(0, self.strip_length-1): self.empty_center() for _ in range(num_of_fires)}
        self.pixels = {idx: RGB() for idx in range(self.strip_length)}

    def empty_center(self):
        return dict(color=RGB(random=True), tail=[], step=0)

    def set(self, index, rgb, **kwargs):

        super().set(index, rgb.c, rgb.r, rgb.b, rgb.b)

    def fill(self):

        loss_weight = 1.3
        center_copy = deepcopy(self.centers)

        # for every center in the list
        for c, attr in center_copy.items():

            # get the color and the tail
            color = attr["color"]
            step=attr["step"]
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
                attr["tail"]= list(set( attr["tail"]))

            # if the center has faded then the tails need to fade too
            else:
                # if there are some non zero tail
                if len( attr["tail"]) > 0:
                    # for every tail
                    for t in  attr["tail"]:
                        # get previous, next and index
                        p = t[0]
                        n = t[1]
                        idx = t[2]
                        # estimate ci as before
                        ci = bound_sub(255, self.loss * (loss_weight * step + 1 - idx))
                        # update
                        color.update_single(c=ci)
                        self.add_update_pixel(p,color)
                        self.add_update_pixel(n,color)
                        # if ci is zero remove point from tail
                        if ci == 0:
                            attr["tail"].pop( attr["tail"].index(t))

                # if the center is faded and it has no more tail
                else:
                    # remove the center
                    self.centers.pop(c)
                    # get another one which is not in the center lists already
                    rd = randint(0, self.strip_length-1)
                    while rd in self.centers.keys():
                        rd = randint(0, self.strip_length-1)
                    # put random color
                    self.centers[rd] = self.empty_center()
                    has_popped=True

            # is the center has been removed then dont update
            if not has_popped:
                self.centers[c]["tail"] = attr["tail"]
                step=circular_step(step,self.strip_length)
                self.centers[c]["step"]=step

        self.update_couter()

        # update pixels with value in list
        for idx, color in self.pixels.items():
            # if c is zero ser led to black
            if color.c==0:
                self.set(idx,RGB())
            else:
                self.set(idx, color)

    def add_update_pixel(self, idx, new_color):

        current_color=self.pixels[idx]



        if current_color.same_color(new_color) or current_color.is_gray()  :
            self.pixels[idx].update_color(new_color)
        elif self.use_add:
            self.pixels[idx].add_colors(new_color)
        else:
            self.pixels[idx].update_color(new_color)



    def update_couter(self):
        self.step += 1
        self.step %= self.strip_length

    def on_loop(self):
        self.fill()
        self.send()
