
from Fillers.Default import Default
from RGB import RGB


class Steady(Default):
    data_type = "Steady"

    def __init__(self, rate):
        """
        Init for steady color
        :param args: for App
        :param trail_length: length of snow trail
        """
        super().__init__(rate)

        self.color = RGB(random=True)
        self.alpha=255


    def fill(self):

        self.color.update_single(c=self.alpha)

        for idx in range(self.strip_length):
            self.color_set(idx,self.color)


