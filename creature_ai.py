import numpy as np
import math
from random import random


def ai_wrapper(c, **kwargs):
    ai_dict = {'dumb': dumb,
               'donkey': donkey}

    ai = ai_dict[c.ai]
    ai(c, **kwargs)


def dumb(c, **kwargs):
    vel = c._velIntensity
    ang = c._velAngle
    da = (random() - 0.5) * math.pi / 50
    c.speed[1] = vel * math.sin(ang + da)
    c.speed[0] = vel * math.cos(ang + da)


def donkey(c, **kwargs):
    vel = c._velIntensity
    if len(c.view) == 0:
        ang = c._velAngle + (random() - 0.5) * math.pi / 50


    else:

        min_dist = math.inf
        nearest_food = None
        for food in c.view:
            dist = math.sqrt((food.pos[0] - c.pos[0]) ** 2 + (food.pos[1] - c.pos[1]) ** 2)

            if dist < min_dist:
                min_dist = dist
                nearest_food = food
        if (nearest_food.pos[0] - c.pos[0]) != 0:
            ang = math.atan((nearest_food.pos[1] - c.pos[1]) / (nearest_food.pos[0] - c.pos[0]))
        else:
            ang = 0
        if (c.pos[0] - nearest_food.pos[0]) > 0:
            ang += math.pi

    c.speed[1] = vel * math.sin(ang)
    c.speed[0] = vel * math.cos(ang)
