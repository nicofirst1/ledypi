import logging

import sympy as sym
from sympy import sympify, lambdify

from patterns.default import Default
from utils.color import scale
from utils.modifier import Modifier

pattern_logger = logging.getLogger("pattern_logger")


class Equation(Default):
    """
    Use user-defined function for the rgb values. The function may depend on :
        - the pixel position in the led strip 'idx'
        - the current timestep 't' which cycles in a predefined allowed range.
        - both
        - none
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.pattern_name = "Equation"

        # max range for function
        self.max_range = self.strip_length * 100

        self.fns = {}

        # r,g,b functions in string format
        self.red_equation = Modifier('red equation', "cos(t)", on_change=self.on_change_red)
        self.green_equation = Modifier('green equation', "idx", on_change=self.on_change_green)
        self.blue_equation = Modifier('blue equation', "sin(t)", on_change=self.on_change_blue)

        # array of colors
        self.rs = []
        self.gs = []
        self.bs = []

        # time step
        self.t = 1

        self.modifiers = dict(
            red_equation=self.red_equation,
            green_equation=self.green_equation,
            blue_equation=self.blue_equation,

        )

        self.generate_colors()

    def on_change_red(self, value):
        assert isinstance(value, str), pattern_logger.warning("The equation value is not a string")
        self.fns['r_fn'] = sympify(value)
        self.generate_colors()

    def on_change_green(self, value):
        assert isinstance(value, str), pattern_logger.warning("The equation value is not a string")
        self.fns['g_fn'] = sympify(value)
        self.generate_colors()

    def on_change_blue(self, value):
        assert isinstance(value, str), pattern_logger.warning("The equation value is not a string")
        self.fns['b_fn'] = sympify(value)
        self.generate_colors()

    def generate_colors(self):
        """
        Generate color out of fill for faster performance
        :return:
        """
        try:
            ts = range(0, self.max_range)
            idxs= range(1, self.max_range-1)

            t,idx = sym.symbols('t,idx')

            rs = lambdify([t, idx], self.fns['r_fn'])
            gs = lambdify([t, idx], self.fns['g_fn'])
            bs = lambdify([t, idx], self.fns['b_fn'])

            rs = rs(ts,idxs)
            gs = gs(ts,idxs)
            bs = bs(ts,idxs)


            # scale in 0,255 values
            rs, gs, bs = self.scale(rs, gs, bs)

            self.rs = rs
            self.gs = gs
            self.bs = bs
        except KeyError:
            pass
        except Exception as e:
            pattern_logger.warning(f"Equation failed to evaluate.\n{e}")

    def fill(self):

        # cicle timestep
        if self.strip_length + self.t >= self.max_range:
            self.t = 1

        # set values
        for idx in range(self.strip_length):
            jdx = idx + self.t
            self.pixels[idx]['color'] = (self.rs[jdx], self.gs[jdx], self.bs[jdx], 255)

        # update timestep
        self.t += 1

    @staticmethod
    def scale(rs, gs, bs):
        """
        Scale and convert to int lists of rgb values
        """

        # get maxs and mins
        r_min = min(rs)
        r_max = max(rs)

        g_min = min(gs)
        g_max = max(gs)

        b_min = min(bs)
        b_max = max(bs)

        # scale
        rs = [scale(r, 0, 255, r_min, r_max) for r in rs]
        gs = [scale(g, 0, 255, g_min, g_max) for g in gs]
        bs = [scale(b, 0, 255, b_min, b_max) for b in bs]

        # convert to int
        rs = [int(elem) for elem in rs]
        gs = [int(elem) for elem in gs]
        bs = [int(elem) for elem in bs]

        return rs, gs, bs
