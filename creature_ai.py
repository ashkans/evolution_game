import numpy as np
import math


def ai_wrapper(c, **kwargs):
    ai_dict = {'dumb': dumb,
               'dumb2': dumb2}

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