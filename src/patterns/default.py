import inspect
import logging
import threading
import time

from rgb import RGB

pattern_logger = logging.getLogger("pattern_logger")


class Default(threading.Thread):

    def __init__(self, handler, rate, pixels, color=RGB()):
        """
        Init for snow effect
        :param args:
        """

        rate /= 100
        threading.Thread.__init__(self)
        self.handler = handler(pixels)
        self.rate = rate

        self.strip_length = pixels
        self.color = color
        self.randomize_color = False
        self.pattern_name = None

        self.pixels = {idx: dict(color=self.color) for idx in range(self.strip_length + 1)}
        self.set_pixels()

    def set_pixels(self):
        for idx in range(self.strip_length):
            self.color_set(idx, self.pixels[idx]['color'])
        self.handler.send()

    def color_set(self, index, rgb, **kwargs):

        self.handler.set(index, rgb.a, rgb.b, rgb.g, rgb.r)

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
                pattern_logger.warn(f"No such attribute named '{k}' for class {self.__str__()}")

        return changed

    def stop(self):
        self.handler.is_stopped = True

    def run(self):

        pattern_logger.info(f"Started pattern: {self.pattern_name}")
        try:
            while not self.handler.is_stopped:
                self.on_loop()
        except KeyboardInterrupt:
            pass

        self.handler.close()
        pattern_logger.info("Stopped pattern")

    def bound_attrs(self):
        """
        override this function if the fill method to bound attributes to a limited range
        :return:
        """
        raise NotImplementedError()

    def set_rate(self, rate):
        rate /= 100
        self.rate = rate
