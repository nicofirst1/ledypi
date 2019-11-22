
from Fillers.Default import Default
from RGB import RGB


class Strobe(Default):
    data_type = "Strobe"

    def __init__(self, rate):
        """
        Init for steady color
        :param args: for App
        :param trail_length: length of snow trail
        """
        super().__init__(rate)

        self.color = RGB(random=True)
        self.delay=10
        self.step=0


    def fill(self):


        if self.color.c>0 and self.step%self.delay!=0:
            self.color.update_single(c=0)
            self.step=0
        if self.color.c == 0 and self.step % self.delay != 0:
            self.color.update_single(c=self.alpha)
            self.step=0

        self.step+=1


        for idx in range(self.strip_length):
            self.color_set(idx,self.color)


