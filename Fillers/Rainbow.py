from DotStar_Emulator.emulator.send_test_data import App
from math import sin, pi, floor

from Fillers.Default import Default
from RGB import RGB
from utils import scale


class Rainbow(Default):

    data_type = "Rainbow"

    def __init__(self, rate, intensity=255):
        """
        Init for FireWork effect
        :param rate:
        """
        super().__init__(rate)

        self.strip_length=self.grid_size.x+self.grid_size.y
        self.counter=0
        self.intensity=intensity
        self.r_div=0
        self.b_div=1
        self.g_div=2
        self.max_range=10
        self.set_pixels()

    def fill(self):

        r_div=self.r_div
        b_div=self.b_div
        g_div=self.g_div

        if not self.r_div == 0:
            r_div = pi/self.r_div
        if not self.b_div == 0:
            b_div = pi/self.b_div
        if not self.g_div == 0:
            g_div = pi/self.g_div


        for idx in range(self.strip_length):

            idx2degree=scale(idx+self.counter,0,self.max_range,0,self.strip_length)

            r=sin(idx2degree+r_div)
            g=sin(idx2degree+g_div)
            b=sin(idx2degree+b_div)

            r=scale(r,0,255,-1,1)
            g=scale(g,0,255,-1,1)
            b=scale(b,0,255,-1,1)

            r=floor(r)
            g=floor(g)
            b=floor(b)

            self.pixels[idx]['color']=RGB(r=r,g=g,b=b,c=self.intensity)


        self.counter+=1
        self.counter%=self.strip_length*3
        self.set_pixels()
