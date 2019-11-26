from Fillers.Default import Default
from RGB import RGB
from utils import bound_sub, bound_add


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
        self.increasing = False
        self.loss = 255

    def fill(self):

        c = self.color.c

        if 0 <= c < 255 and self.increasing:
            c = bound_add(c, self.loss, maximum=255)
        elif 0 < c <= 255 and not self.increasing:
            c = bound_sub(c, self.loss, minimum=0)
        else:
            self.increasing=not self.increasing

        self.color.update_single(c=c)

        for idx in range(self.strip_length):
            self.pixels[idx]['color'] = self.color
