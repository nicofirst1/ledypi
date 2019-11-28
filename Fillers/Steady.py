
from Fillers.Default import Default
from RGB import RGB


class Steady(Default):
    data_type = "Steady"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def fill(self):

        self.color.update_single(c=self.alpha)
        for idx in range(self.strip_length):
            self.pixels[idx]['color']=self.color


