from patterns.default import Default
from rgb import RGB


class Off(Default):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pattern_name = "Off"

    def fill(self):

        for idx in range(self.strip_length):
            self.pixels[idx]['color'] = RGB()
