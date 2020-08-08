from utils.color import scale


class Modifier:
    """
    Modifier class used for variable attributes in the Patterns
    """

    def __init__(self, name, value, minimum=None, maximum=None, options=None, on_change=None):
        """

        :param name: str, the name of the modifier, the one shown in the interfaces
        :param value: obj, the value
        :param minimum: optional int, min factor for scaling
        :param maximum:  optional int, max factor for scaling
        :param options: optional list, list of possible options for value
        """

        self.on_change = on_change

        if options is None:
            self.type = type(value)
        else:
            self.type = list

        self.min = minimum
        self.max = maximum
        self.options = options
        self.name = name
        self.value = value

    def __call__(self, inverse=False):
        """
        Return the value when called
        :param inverse: bool, if to return self.max - val or just val
        """

        if inverse:
            return self.max - self.value

        else:

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

        if self.type == int or self.type == float:

            if self.min is not None and self.max is not None:
                self._value = self.type((scale(value, self.min, self.max, 0, 100)))
            else:
                raise ValueError(f"You did not set a valid max/min for the modifier {self.name}")

        elif self.type == list:

            # check if the value is valid
            assert value in self.options, f"Value '{value}' is not in the list of possible options: {self.options}"
            self._value = value

        else:
            self._value = value

        if self.on_change is not None:
            self.on_change(value)
