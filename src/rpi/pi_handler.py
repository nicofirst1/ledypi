from utils.color import scale_brightness

PIN = 18


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

        if index is not None and index < self.pixel_count:
            # scale the rgb value by the intensity
            r = scale_brightness(r, a)
            g = scale_brightness(g, a)
            b = scale_brightness(b, a)
            # create color and set it
            color = (r, g, b)
            self.np[index] = color

    def send(self):

        self.np.show()

    def on_loop(self):
        raise NotImplementedError

    def close(self):
        self.np.deinit()
        print("Closing PiHandler")

