import inspect
import time
import threading
from DotStar_Emulator.emulator.send_test_data import App

from RGB import RGB


class Default(App,threading.Thread ):
    data_type = ""

    def __init__(self, delay, color=RGB()):
        """
        Init for snow effect
        :param args:
        """

        delay /= 100
        threading.Thread.__init__(self)
        super().__init__(delay)
        self.rate = delay

        self.strip_length = self.grid_size.x + self.grid_size.y - 1
        self.alpha = 255
        self.color = color
        self.pixels = {idx: dict(color=self.color) for idx in range(self.strip_length + 1)}
        self.set_pixels()


    def set_pixels(self):
        for idx in range(self.strip_length):
            self.color_set(idx, self.pixels[idx]['color'])
        self.send()

    def color_set(self, index, rgb, **kwargs):

        super().set(index, rgb.c, rgb.b, rgb.g, rgb.r)

    def fill(self):

        raise NotImplementedError

    def on_loop(self):
        self.fill()
        self.set_pixels()
        time.sleep(self.rate)

    def update_args(self, **kwargs):
        variables = [i for i in dir(self) if not inspect.ismethod(i)]

        changed = False
        for k in kwargs.keys():
            if k in variables:
                setattr(self, k, kwargs[k])
                changed = True

        if not changed:
            for k in kwargs.keys():
                print(f"No such attribute named '{k}' for class {self.__str__()}")

        return changed

    def stop(self):
        self.is_stopped = True

    def run(self):
        try:
            while not self.is_stopped:
                self.on_loop()
        except KeyboardInterrupt:
            pass

        super().close_connetcion()