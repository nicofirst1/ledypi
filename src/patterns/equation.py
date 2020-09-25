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
        self.max_range = self.strip_length * 1000

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

    def on_change_red(self, value):
        assert isinstance(value, str), pattern_logger.warning("The equation value is not a string")
        self.fns['r_fn'] = sympify(value)

    def on_change_green(self, value):
        assert isinstance(value, str), pattern_logger.warning("The equation value is not a string")
        self.fns['g_fn'] = sympify(value)

    def on_change_blue(self, value):
        assert isinstance(value, str), pattern_logger.warning("The equation value is not a string")
        self.fns['b_fn'] = sympify(value)

    def fill(self):

        # cicle timestep
        if self.strip_length + self.t >= self.max_range:
            self.t = 1
        try:
            ts = range(self.t, self.t + self.strip_length)
            idxs = range(len(ts))

            t, idx = sym.symbols('t,idx')

            rs = lambdify([t, idx], self.fns['r_fn'])
            gs = lambdify([t, idx], self.fns['g_fn'])
            bs = lambdify([t, idx], self.fns['b_fn'])

            rs = rs(ts, idxs)
            gs = gs(ts, idxs)
            bs = bs(ts, idxs)

            # scale in 0,255 values
            rs, gs, bs = self.scale(rs, gs, bs)

            # set values
            for idx in range(self.strip_length):
                self.pixels[idx]['color'] = (rs[idx], gs[idx], bs[idx], 255)

        except Exception as e:
            pattern_logger.warning(f"Equation failed to evaluate.\n{e}")

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
