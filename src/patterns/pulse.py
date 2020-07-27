from patterns.default import Default
from utils.color import bound_sub, bound_add


class Pulse(Default):
    """
    Turno on\off the strip with a specific speed
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.increasing = False
        self.speed = 255
        self.pattern_name = "Pulse"

        self.modifiers = dict(
            loss=self.speed,
        )

    def fill(self):

        a = self.color.a

        if 0 <= a < 255 and self.increasing:
            a = bound_add(a, self.speed, maximum=255)
        elif 0 < a <= 255 and not self.increasing:
            a = bound_sub(a, self.speed, minimum=0)
        else:
            self.increasing = not self.increasing

        self.color.update_single(a=a)

        for idx in range(self.strip_length):
            self.pixels[idx]['color'] = self.color
