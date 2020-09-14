from patterns.default import Default
from utils.rgb import RGB


class Off(Default):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pattern_name = "Off"

    def fill(self):
        self.rate.value = 100
        for idx in range(self.strip_length):
            self.pixels[idx]['color'] = RGB()
