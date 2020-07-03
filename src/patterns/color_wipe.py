from patterns.default import Default
from rgb import RGB


class ColorWipe(Default):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.step = 1
        self.reverse = False
        self.pattern_name = "ColorWipe"

    def fill(self):

        step = self.step
        color = self.color

        if self.reverse:
            color = RGB()

        for idx in range(self.strip_length):
            if idx < step:
                self.pixels[idx]['color'] = color

        self.step += 1

        if self.step > self.strip_length:
            self.reverse = not self.reverse
            self.step = 0
