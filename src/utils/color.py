import math
from random import randint


def scale(old_val, new_min, new_max, old_min, old_max):
    old_range = (old_max - old_min)
    if old_range == 0: old_range += 1e-100
    new_range = (new_max - new_min)
    new_value = (((old_val - old_min) * new_range) / old_range) + new_min
    return new_value


def random_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))


def bound_sub(value, to_sub, minimum=0):
    value -= to_sub
    if value < minimum: return minimum
    return math.floor(value)


def bound_add(value, to_add, maximum=255):
    value += to_add
    if value > maximum: return maximum
    return math.ceil(value)


def circular_step(step, maximum):
    step += 1
    return step % maximum
