import time


from DotStar_Emulator.emulator.send_test_data import App

from RGB import RGB
from utils import bound_sub, circular_step
import inspect

class Default(App):
    data_type = ""

    def __init__(self, rate):
        """
        Init for snow effect
        :param args:
        """

        rate*=100
        super().__init__(rate)

        self.strip_length = self.grid_size.x + self.grid_size.y - 1
        self.alpha=255
        self.pixels={idx:dict(color=RGB()) for idx in range(self.strip_length+1)}

    def set_pixels(self):
        for idx in range(self.strip_length):
            self.color_set(idx, self.pixels[idx]['color'])
        self.send()

    def color_set(self, index, rgb, **kwargs):

        super().set(index, rgb.c, rgb.b, rgb.g, rgb.r)
        time.sleep(self.rate)




    def fill(self):

       raise NotImplementedError


    def on_loop(self):
        self.fill()
        self.send()

    def update_args(self, **kwargs):
        variables = [i for i in dir(self) if not inspect.ismethod(i)]

        changed=False
        for k in kwargs.keys():
            if k in variables:
                setattr(self, k, kwargs[k])
                changed=True

        if not changed:
            for k in kwargs.keys():
                print(f"No such attribute named '{k}' for class {self.__str__()}")

        return changed



    def stop(self):
        self.is_stopped=True