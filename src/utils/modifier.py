from utils.color import scale


class Modifier:

    def __init__(self, name, value, minimum=None, maximum=None):

        self.type = type(value)
        self.min = minimum
        self.max = maximum
        self.name = name
        self.value = value

    def __call__(self, *args, **kwargs):
        """
        Return the value when called
        :param args:
        :param kwargs:
        :return: self.value
        """
        return self.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """
        When setting, scale if int
        :param value:
        :return:
        """

        if self.type == int or self.type==float:
            if self.min is not None and self.max is not None:
                self._value = self.type((scale(value, self.min, self.max, 0, 100)))
            else:
                raise ValueError(f"You did not set a valid max/min for the modifier {self.name}")

        else:
            self._value = value
