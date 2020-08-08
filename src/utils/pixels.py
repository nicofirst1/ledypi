class Pixel(dict):
    """
    Pixel class to store information about a pixel
    """

    def __init__(self, index, set_func, **kwargs):
        """
        Save set function and index
        :param index: int, pixel index in the strip
        :param set_func: function, handler function to set color
        """
        self.set_func = set_func
        self.index = index

        super(Pixel, self).__init__(**kwargs)

    def __setitem__(self, key, value):
        """
        Override set item to call set function first
        """
        # call function only if the color has change
        if key == 'color':
            self.set_func(self.index, value)

        super(Pixel, self).__setitem__(key, value)
