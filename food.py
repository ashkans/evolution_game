from thing import Thing, Things
from random import random
from random import randint
from config import SETTING


class Food(Thing):

    def __init__(self, **kwargs):

        if 'imgName' not in kwargs.keys():
            kwargs['imgName'] = 'square'
        Thing.__init__(self, **kwargs)
        self.rotationRate = random() * 0.001
        self.energyContent = 10
        self.eaten_by = []

    def otherUpdates(self, dt):
        numCreaturesWhoEat = len(self.eaten_by)
        if len(self.eaten_by) != 0:
            for c in self.eaten_by:
                c.eat(self.energyContent / numCreaturesWhoEat)
            self.eaten()
        self.rotate(dt=dt)

    def eaten(self):
        self.kill()


class Foods(Things):
    def __init__(self, **kwargs):
        Things.__init__(self, **kwargs)
        self.timeFromLastSpawn = 0

    def add_food(self, dt):
        self.timeFromLastSpawn += dt
        x = randint(1, SETTING['DISPLAY']['MAIN_SCREEN_RES']['WIDTH'])
        y = randint(1, SETTING['DISPLAY']['MAIN_SCREEN_RES']['HEIGHT'])

        if self.timeFromLastSpawn > SETTING['FOOD']['RATE']:
            self.add(Food(imgName='apple', still=True, size=30, pos=[x, y]))
            self.timeFromLastSpawn = 0
