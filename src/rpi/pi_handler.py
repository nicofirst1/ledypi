PIN = 18


class PiHandler(object):
    """
    Hanlder fot the rapberrypi and led control
    """

    def __init__(self, pixels):
        # the imports must be hidden since they won't work on pc
        from neopixel import NeoPixel
        import board

        # init the pixel strip
        self.np = NeoPixel(board.D18, pixels, auto_write=False)
        self.pixel_count = pixels
        self.is_stopped = False

    def set(self, index, c, b, g, r):

        if index is not None and index < self.pixel_count:
            # scale the rgb value by the intensity
            r = scale(r, c)
            g = scale(g, c)
            b = scale(b, c)
            # create color and set it
            color =(r, g, b)
            self.np[index]= color

    def send(self):

        self.np.show()

    def on_loop(self):
        raise NotImplementedError

    def close(self):
        for index in range(self.pixel_count):
            self.np[index]= (0,0,0)
        self.np.show()


def scale(value, brightness):
    brightness /= 255
    return int(value * brightness)
