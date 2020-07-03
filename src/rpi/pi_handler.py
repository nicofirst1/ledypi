PIN = 18


class PiHandler(object):
    data_type = None

    def __init__(self, pixels):
        from rpi_ws281x import PixelStrip

        self.np = PixelStrip(pixels, PIN)
        self.np.begin()
        self.pixel_count = pixels
        self.is_stopped = False

    def set(self, index, c, b, g, r):
        from rpi_ws281x import Color

        if index is not None and index < self.pixel_count:
            r = scale(r, c)
            g = scale(g, c)
            b = scale(b, c)
            color = Color(r, g, b)
            self.np.setPixelColor(index, color)

    def send(self):

        self.np.show()

    def on_loop(self):
        raise NotImplementedError

    def close(self):
        for index in range(self.pixel_count):
            self.np.setPixelColor(index, 0)
        self.np.show()


def scale(value, brightness):
    brightness /= 255
    return int(value * brightness)
