class PiHandler(object):
    """
    Hanlder fot the rapberrypi and led control
    """

    def __init__(self, pixels):
        # the imports must be hidden since they won't work on pc
        import neopixel
        import board

        # init the pixel strip
        self.np = neopixel.NeoPixel(board.D18, pixels, auto_write=False)
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
        self.np.fill((0, 0, 0, 0))
        self.np.deinit()
        print("Closing PiHandler")
