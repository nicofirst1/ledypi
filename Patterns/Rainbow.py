from DotStar_Emulator.emulator.send_test_data import App
from math import sin, pi, floor

from Patterns.Default import Default
from RGB import RGB
from utils import scale


class Rainbow(Default):

    data_type = "Rainbow"

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.counter=0
        self.intensity=255
        self.r_phi=0
        self.b_phi=1
        self.g_phi=2
        self.max_range=1
        self.set_pixels()

    def fill(self):

        r_phi=self.r_phi
        b_phi=self.b_phi
        g_phi=self.g_phi

        if not self.r_phi == 0:
            r_phi = pi/self.r_phi
        if not self.b_phi == 0:
            b_phi = pi/self.b_phi
        if not self.g_phi == 0:
            g_phi = pi/self.g_phi


        for idx in range(self.strip_length):

            idx2degree=scale(idx+self.counter,0,self.max_range,0,self.strip_length)

            r=sin(idx2degree+r_phi)
            g=sin(idx2degree+g_phi)
            b=sin(idx2degree+b_phi)

            r=scale(r,0,255,-1,1)
            g=scale(g,0,255,-1,1)
            b=scale(b,0,255,-1,1)

            r=floor(r)
            g=floor(g)
            b=floor(b)

            self.pixels[idx]['color']=RGB(r=r,g=g,b=b,c=self.intensity)

        self.counter+=1
        self.counter%=self.strip_length*255

