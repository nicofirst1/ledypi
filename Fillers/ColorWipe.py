
from Fillers.Default import Default
from RGB import RGB


class ColorWipe(Default):
    data_type = "ColorWipe"

    def __init__(self, delay, color='rand'):
        """
        Init for steady color
        :param args: for App
        :param trail_length: length of snow trail
        """
        super().__init__(delay)

        if color=="rand":
            color=RGB(random=True)

        self.color = color
        self.step=1
        self.reverse=False


    def fill(self):

        self.color.update_single(c=self.alpha)

        step=self.step
        color=self.color

        if self.reverse:
            color=RGB()

        for idx in range(self.strip_length):
            if idx< step:
                self.pixels[idx]['color']=color


        self.step+=1

        if self.step>self.strip_length :
            self.reverse=not self.reverse
            self.step=0


