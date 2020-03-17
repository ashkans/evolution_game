import numpy as np
import math
from random import random


def ai_wrapper(c, **kwargs):
    ai_dict = {'dumb': dumb,
               'dumb2': dumb2,
               'donkey': donkey,
               'Test': Test}

    ai = ai_dict[c.ai]
    ai(c, **kwargs)


def dumb(c, **kwargs):
    c.azimuth += (np.random.random() - 0.5) * math.pi / 50
    c.azimuth = math.fmod(c.azimuth, 2 * math.pi)
    c.v += (np.random.random() - 0.5) / 100


def dumb2(c, **kwargs):
    c.azimuth += (np.random.random() - 0.5) * math.pi / 50
    c.azimuth = math.fmod(c.azimuth, 2 * math.pi)
    c.v += (np.random.random() - 0.5) / 100


def Test(c, **kwargs):
    vel = c._velIntensity
    ang = c._velAngle
    da = (random() - 0.5) * .01
    c.speed[1] = vel * math.sin(ang + da)
    c.speed[0] = vel * math.cos(ang + da)


def donkey(c, **kwargs):
    if len(c.view) == 0:
        c.azimuth += (np.random.random() - 0.5) * math.pi / 50
        c.azimuth = math.fmod(c.azimuth, 2 * math.pi)
        c.v += (np.random.random() - 0.5) / 100
    else:

        min_dist = math.inf
        nearest_food = None
        for food in c.view:
            dist = math.sqrt((food.x - c.x) ** 2 + (food.y - c.y) ** 2)

            if dist < min_dist:
                min_dist = dist
                nearest_food = food
        if (nearest_food.y - c.y) != 0:
            c.azimuth = math.atan((nearest_food.x - c.x) / (nearest_food.y - c.y))
        if (c.y - nearest_food.y) > 0:
            c.azimuth += math.pi
