import random
from collections import OrderedDict

import matplotlib.cm

from patterns.default import Default
from utils.modifier import Modifier

cmaps = OrderedDict()
cmaps['Perceptually Uniform Sequential'] = [
    'viridis', 'plasma', 'inferno', 'magma', 'cividis']

cmaps['Sequential'] = [
    'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
    'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
    'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

cmaps['Sequential (2)'] = [
    'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
    'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
    'hot', 'afmhot', 'gist_heat', 'copper']

cmaps['Diverging'] = [
    'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
    'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']

cmaps['Cyclic'] = ['twilight', 'twilight_shifted', 'hsv']

cmaps['Qualitative'] = ['Pastel1', 'Pastel2', 'Paired', 'Accent',
                        'Dark2', 'Set1', 'Set2', 'Set3',
                        'tab10', 'tab20', 'tab20b', 'tab20c']

cmaps['Miscellaneous'] = [
    'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
    'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
    'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']

new_cmap = []
for k, v in cmaps.items():
    new_cmap += [f"{k}: {elem}" for elem in v]

cmaps = new_cmap


class ColorMap(Default):
    """
    Use perlin noise together with rgb mapping
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.pattern_name = "ColorMap"

        self.cmap_name = Modifier('cmap name', random.choice(cmaps), options=cmaps, on_change=self.init_cmap)
        self.cmap = None
        self.init_cmap(self.cmap_name())

        self.lower_bound = Modifier('lower', 0, minimum=0, maximum=self.strip_length)
        self.upper_bound = Modifier('upper', 0, minimum=0, maximum=self.strip_length)

        self.specular = Modifier('specular', False)

        self.rate.value = 100

        self.modifiers = dict(
            cmap_name=self.cmap_name,
            lower_bound=self.lower_bound,
            upper_bound=self.upper_bound,
            specular=self.specular,

        )



    def init_cmap(self, name):
        """
        Change the current color map and set max to number of pixels
        :return:
        """
        name = name.split(":")[1].strip()
        cmap = matplotlib.cm.get_cmap(name)

        def cmap_func(idx):
            idx = idx - self.lower_bound() + self.upper_bound()
            idx /= self.strip_length

            return cmap(idx)

        self.cmap = cmap_func

    def fill(self):

        if not self.specular():
            for idx in range(self.strip_length):
                r, g, b, a = [elem * 255 for elem in self.cmap(idx)]
                self.pixels[idx]['color'] = (r, g, b, a)
        else:

            for idx in range(self.strip_length // 2):
                r, g, b, a = [elem * 255 for elem in self.cmap(idx)]
                self.pixels[idx]['color'] = (r, g, b, a)

            for idx in range(idx, self.strip_length):
                jdx = self.strip_length - idx
                r, g, b, a = [elem * 255 for elem in self.cmap(jdx)]
                self.pixels[idx]['color'] = (r, g, b, a)
