import logging
from random import random

from patterns.default import Default
from utils.rgb import RGB

pattern_logger = logging.getLogger("pattern_logger")


class GameOfLife(Default):
    """
    Game of life using the rules on wiki
    https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.pattern_name = "GameOfLife"
        self.alive = Alive(size=self.strip_length)
        self.num_alives = [0] * self.strip_length
        self.randomize_color = True

    def fill(self):

        # update alive nums
        self.num_alives.append(sum(self.alive))
        self.num_alives.pop(0)

        for idx in range(self.strip_length):
            # get the alive neighbors
            n = sum(self.alive[idx - 4:idx]) + sum(self.alive[idx:idx + 4])
            cur = self.alive[idx]

            # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
            # Any live cell with more than three live neighbours dies, as if by overpopulation.
            if cur and (n < 2 or n > 3):
                self.alive[idx] = 0
                self.color_idx(idx)

            # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
            elif not cur and n == 3:
                self.alive[idx] = 1
                self.color_idx(idx)

            # Any live cell with two or three live neighbours lives on to the next generation.

        # check if the number of alive players has not changed in an entire execution
        if self.num_alives[1:] == self.num_alives[:-1]:
            self.alive = Alive(self.strip_length)
            # shut down 
            self.color_all((0, 0, 0, 0))
            pattern_logger.debug("Game of Life reset")

    def color_idx(self, idx):
        # if the current one is alive then color it
        if self.alive[idx]:
            if self.randomize_color:
                self.pixels[idx]['color'] = RGB(random=True)
            else:
                self.pixels[idx]['color'] = self.color
        # else kill it
        else:
            self.pixels[idx]['color'] = (0, 0, 0, 0)


class Alive(list):
    """
    Custom extension of the list class, implements easier slicing for circular buffer
    """

    def __init__(self, size, *args):
        list.__init__(self, *args)
        for _ in range(size):
            self.append(1 if random() > 0.5 else 0)

    def __getitem__(self, index):

        if isinstance(index, int):
            return super(Alive, self).__getitem__(index % len(self))
        elif isinstance(index, slice):
            start = index.start
            stop = index.stop

            if start < 0:
                ret = super(Alive, self).__getitem__(slice(start, len(self), index.step))
                return super(Alive, self).__getitem__(slice(0, stop, index.step)) + ret

            elif stop > len(self):
                ret = super(Alive, self).__getitem__(slice(start, len(self), index.step))
                return super(Alive, self).__getitem__(slice(0, stop % len(self), index.step)) + ret
            else:
                return super(Alive, self).__getitem__(index)
