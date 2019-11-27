import numpy as np
import math


def eye_wrapper(c, pop, food, **kwargs):
    eye_dict = {'blind': blind,
                'blind2': blind2}

    eye = eye_dict[c.eye]
    eye(c, **kwargs)


def blind(c, **kwargs):
    c.sight = 0
    c.view = []
    c.seeing_ec = 0


def blind2(c, **kwargs):
    c.sight = c.energy
    c.view = []
    c.seeing_ec = 0
