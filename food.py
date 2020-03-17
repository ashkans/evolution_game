from thing import Thing, Things
from random import random


class Food(Thing):

    def __init__(self, **kwargs):

        if 'imgName' not in kwargs.keys():
            kwargs['imgName'] = 'square'
        Thing.__init__(self, **kwargs)
        self.rotationRate = random() * 0.001

    def otherUpdates(self, dt):
        self.rotate(dt=dt)


class Foods(Things):
    pass
