from random import randint

from Fillers.Default import Default
from RGB import RGB


class Meteor(Default):
    data_type = "Meteor"
    def __init__(self, rate,size=10,  trail_decay=64,  random_decay=True):
        """
        Init for steady color
        :param args: for App
        :param trail_length: length of snow trail
        """
        super().__init__(rate)

        self.color = RGB(random=True)
        self.size=size
        self.trail_decay=trail_decay
        self.random_decay=random_decay


    def fill(self):


        for idx in range(self.strip_length*2):

            for jdx in range(self.strip_length):
                if not self.random_decay or randint(0,10) > 5:
                    self.pixels[jdx]['color'].fade(self.trail_decay)

            for jdx in range( 0, self.size):
                if idx-jdx< self.strip_length and idx-jdx>=0:
                    self.pixels[idx-jdx]['color']=self.color.copy()


            self.set_pixels()



