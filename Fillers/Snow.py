
from Fillers.Default import Default


class Snow(Default):
    data_type = "Snow"

    def __init__(self, args, trail_length=5):
        """
        Init for snow effect
        :param args: for App
        :param trail_length: length of snow trail
        """
        super().__init__(args)

        self.trail = trail_length
        self.min_space = 3  # min space between trail end and trail start
        self.counter = 0

    def fill(self):

        # get the number of trails the strip can have
        num_of_trail = self.strip_length // (self.trail + self.min_space)
        # make them even
        if num_of_trail % 2 != 0:
            num_of_trail -= 1

        intensity = 255
        loss = intensity // self.trail  # loss of intensity for trail

        for jdx in reversed(range(num_of_trail)):
            for idx in range(jdx + self.counter, self.strip_length + jdx + self.counter, num_of_trail):
                self.set(idx % self.strip_length, intensity, 255, 255, 255)
            if not intensity - loss < 0:
                intensity -= loss
            else:
                intensity = 0

        self.update_counter()

    def update_counter(self):
        self.counter += 1
        self.counter %= self.strip_length
