import numpy as np
import math


def eye_wrapper(c, pop, foods, **kwargs):
    eye_dict = {'see_foods_loc': see_foods_loc}

    eye = eye_dict[c.eye]
    eye(c, pop, foods, **kwargs)


def see_foods_loc(c, pop, foods, **kwargs):
    if c.sight < 0:
        c.sight = 0
    # c.seeing_ec = c.sight / 1e3

    c.view = []
    for food in foods:
        if math.sqrt((food.pos[0] - c.pos[0]) ** 2 + (food.pos[1] - c.pos[1]) ** 2) < c.sight:
            c.view.append(food)

