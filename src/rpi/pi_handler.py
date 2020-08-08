class PiHandler(object):
    """
    Hanlder fot the rapberrypi and led control
    """

    def __init__(self, pixels):
        # the imports must be hidden since they won't work on pc
        import neopixel
        import board

        # init the pixel strip
        self.np = neopixel.NeoPixel(board.D18, pixels, auto_write=False, pixel_order=neopixel.RGB)
        self.pixel_count = pixels

    def set(self, index, a, b, g, r):

        try:
            # create color and set it
            color = (r, g, b)
            self.np[index] = color
        except IndexError:
            print("error")

    def send(self):
        self.np.show()

    def close(self):
        self.np.fill((0, 0, 0, 0))
        self.np.deinit()
        print("Closing PiHandler")
