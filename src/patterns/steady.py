from patterns.default import Default
from rgb import RGB


class Steady(Default):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pattern_name= "Steady"

    def fill(self):

        if self.randomize_color:
            color = RGB(random=True)
        else:
            color = self.color

        color.update_single(a=self.alpha)
        for idx in range(self.strip_length):
            self.pixels[idx]['color'] = self.color
