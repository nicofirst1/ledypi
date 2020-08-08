from patterns.default import Default


class Steady(Default):
    """
    Steady color
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pattern_name = "Steady"

    def fill(self):

        for idx in range(self.strip_length):
            self.pixels[idx]['color'] = self.color
