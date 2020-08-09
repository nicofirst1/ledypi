LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53


class NeoPixel(object):
    """
    Hanlder fot the rapberrypi and led control
    """

    def __init__(self, pixels):
        # the imports must be hidden since they won't work on pc
        from rpi_ws281x import PixelStrip

        # init the pixel strip
        self.np = PixelStrip(pixels, 18, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.np.begin()
        self.pixel_count = pixels

    def set(self, index, a, b, g, r):
        """
        Set the a pixel color
        :param index: int, the pixel index
        :param a: int, the alpha value, add for compatibility
        :param b: int, blue value
        :param g:  int, green value
        :param r:  int, red value
        :return:
        """
        from rpi_ws281x import Color
        try:
            # create color and set it
            color = Color(r, g, b)
            self.np.setPixelColor(index, color)
        except IndexError:
            print("error")

    def send(self):
        """
        Show the colors
        :return:
        """
        self.np.show()

    def close(self):
        """
        Set the strip to black and disconnect
        :return:
        """
        from rpi_ws281x import Color

        c = Color(0, 0, 0)
        for idx in range(self.pixel_count):
            self.np.setPixelColor(idx, c)
        self.np.show()
        self.np._cleanup()
        print("Closing PiHandler")


class Dotstar(object):
    """
    Hanlder fot the rapberrypi and led control
    """

    def __init__(self, pixels):
        # the imports must be hidden since they won't work on pc
        import board
        import adafruit_dotstar

        self.np = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, pixels, auto_write=True, )

        self.pixel_count = pixels

    def set(self, index, a, b, g, r):
        """
        Set the a pixel color
        :param index: int, the pixel index
        :param a: int, the alpha value, add for compatibility
        :param b: int, blue value
        :param g:  int, green value
        :param r:  int, red value
        :return:
        """
        try:
            # create color and set it
            color = (r, g, b)
            self.np[index] = color
        except IndexError:
            print("error")

    def send(self):
        """
        Show the colors
        :return:
        """
        self.np.show()

    def close(self):
        """
        Set the strip to black and disconnect
        :return:
        """

        c = (0, 0, 0)
        for idx in range(self.pixel_count):
            self.np[idx] = c
        self.np.show()
        self.np.deinit()
        print("Closing PiHandler")
