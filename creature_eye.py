import numpy as np
import math


def eye_wrapper(c, pop, foods, **kwargs):
    eye_dict = {'blind': blind,
                'blind2': blind2,
                'see_foods_loc': see_foods_loc,
                'see_foods_loc2': see_foods_loc2}

    eye = eye_dict[c.eye]
    eye(c, pop, foods, **kwargs)


def blind(c, pop, foods, **kwargs):
    c.sight = 0
    c.view = []
    c.seeing_ec = 0


def blind2(c, pop, foods, **kwargs):
    c.sight = c.energy
    c.view = []
    c.seeing_ec = 0


def see_foods_loc(c, pop, foods, **kwargs):
    if c.sight < 0:
        c.sight = 0
    c.seeing_ec = c.sight / 1e3

    c.view = []
    for food in foods.contents:
        if math.sqrt((food.x - c.x) ** 2 + (food.y - c.y) ** 2) < c.sight:
            c.view.append(food)


def see_foods_loc2(c, pop, foods, **kwargs):
    if c.sight < 0:
        c.sight = 0
    c.seeing_ec = c.sight / 1e3

    c.view = []
    for food in foods.contents:
        if math.sqrt((food.x - c.x) ** 2 + (food.y - c.y) ** 2) < c.sight:
            c.view.append(food)
