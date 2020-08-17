import inspect
import logging
import threading
import time

import numpy as np

from utils.modifier import Modifier
from utils.pixels import Pixel
from utils.rgb import RGB

pattern_logger = logging.getLogger("pattern_logger")


class Default(threading.Thread):
    """
    The default class for patterns
    """

    def __init__(self, handler, rate, pixels, color=RGB()):
        """

        :param handler: The handler for the led strip, either a DotStar_Emulator.emulator.send_test_data.App or a rpi.pi_handler.PiHandler
        :param rate:(float) the rate for the pixel update
        :param pixels: (int) the number of pixels
        :param color: (default RGB), the initial color for the leds
        """

        # init the thread and the handler
        threading.Thread.__init__(self, name="PatternThread")

        self.handler = handler
        self.rate = Modifier("rate", float(rate), minimum=0.0, maximum=1.5)
        self.stop = False

        self.strip_length = pixels
        self.color = color
        self.alpha = 255

        # boolan value to randomize color
        self.randomize_color = False

        # string for patter name
        self.pattern_name = None

        # dictionary storing the modifiers to be implemented in the web app
        self.modifiers = dict()

        # init and set the pixels to the default color
        self.pixels = {idx: Pixel(index=idx, color=self.color.copy(), set_func=self.color_set) for idx in
                       range(self.strip_length + 1)}

    def show(self):
        """
        Set the color of the strip using the handler and show
        :return:
        """

        self.handler.send()

    def color_all(self, color):
        """
        Color all the pixels with the same color (useful to set all black)
        :param color: rgba values
        :return:
        """
        for idx in range(self.strip_length):
            self.pixels[idx]['color'] = color

    def color_set(self, index, rgb):
        """
        Set the color for the specified pixel
        :param index: int, indices of the pixel in range [0, strip_length]
        :param rgb: RGB class or tuple, the rgba values
        :return:
        """

        # extract the values
        try:

            rgb = rgb.scale()

        except AttributeError:
            # if the rgb value is not of RGB class then it should be a tuple, check if it has length 4 first
            assert len(rgb) == 4, "The length of the color should be 4"
            # get and normalize a
            a = rgb[-1] / 255
            # scale for alpha
            rgb = np.multiply(rgb[:-1], a, casting='unsafe').astype(int)

        # scale rgb based on passed alpha
        r, g, b = np.multiply(rgb, self.alpha / 255, casting='unsafe')

        # set with handler
        self.handler.set(index=index, r=int(r), g=int(g), b=int(b), a=self.alpha)

    def fill(self):
        """
        Override this method for your custom patterns
        :return:
        """

        raise NotImplementedError

    def on_loop(self):
        """
        Function called once every loop.
        It updates the pixel colors in the fill method and set them with set pixels
        :return:
        """
        self.fill()
        self.show()
        time.sleep(self.rate())

    def update_args(self, **kwargs):

        variables = [i for i in dir(self) if not inspect.ismethod(i)]

        changed = True
        for k in kwargs.keys():
            # check if the keys are in the modifiers dict
            if k in self.modifiers.keys():
                self.modifiers[k].value = kwargs[k]
            # check if there are some attributes of the class
            elif k in variables:
                setattr(self, k, kwargs[k])

            else:
                changed = False

        if not changed:
            for k in kwargs.keys():
                pattern_logger.warn(f"No such attribute named '{k}' for class {self.__str__()}")

        return changed

    def close(self):
        """
        Close the current pattern
        :return:
        """
        self.stop = True
        pattern_logger.info(f"Pattern {self.pattern_name} stopped")

    def run(self):
        # init handler and set pixels

        self.show()

        pattern_logger.info(f"Started pattern: {self.pattern_name} with rate: {self.rate()}")
        try:
            while not self.stop:
                self.on_loop()
        except KeyboardInterrupt:
            pattern_logger.info("Pattern has been interrupted")
        finally:
            self.close()

    def set_rate(self, rate):
        self.rate.value = rate
