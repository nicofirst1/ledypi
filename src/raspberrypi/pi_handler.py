PIN = 18


class PiHandler(object):
    data_type = None

    def __init__(self, pixels):
        from rpi_ws281x import PixelStrip

        self.np= PixelStrip(pixels,PIN)
        self.np.begin()
        self.pixel_count=pixels
        self.is_stopped=False

        print("Initiated rpi_ws281x" )

    def set(self, index, c, b, g, r):
        from rpi_ws281x import Color

        if index is not None and index < self.pixel_count:
            color = Color(r, g, b, white=c)
            self.np.setPixelColor(index, color)

    def send(self):

        self.np.show()

    def on_loop(self):
        raise NotImplementedError

    def close_connection(self):

        for index in range(self.pixel_count):
            self.np.setPixelColor(index, 0)
        self.np.show()




