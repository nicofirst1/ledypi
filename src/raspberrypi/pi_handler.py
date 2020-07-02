

PIN=18
class PiHandler(object):
    data_type = None

    def __init__(self, pixels):
        from rpi_ws281x import PixelStrip


        self.np= PixelStrip(pixels,PIN)
        self.np.begin()
        self.pixel_count=pixels


        print("Data Type:", self.data_type)

    def set(self, index, c, b, g, r):
        if index is not None and index < self.pixel_count:
            self.np.setPixelColorRGB(index, r,g,b,c)



    def send(self):

        self.np.show()

    def on_loop(self):
        raise NotImplementedError



