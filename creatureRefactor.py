from thing import Thing, Things
from random import random
from creature_ai import ai_wrapper
from creature_eye import eye_wrapper
import pygame


class Creature(Thing):

    def __init__(self, energy=None, ai=None, sight=None, eye=None, basic_ec=None, seeing_ec=None, speed_ec=None,
                 **kwargs):

        if 'imgName' not in kwargs.keys():
            kwargs['imgName'] = 'bob'
        Thing.__init__(self, **kwargs)

        if ai is None:
            ai = 'Test'
        if sight is None:
            sight = 0

        if eye is None:
            eye = 'see_foods_loc'

        if basic_ec is None:
            basic_ec = 0

        if seeing_ec is None:
            seeing_ec = 0

        if speed_ec is None:
            speed_ec = 0

        self.energy = energy
        self.ai = ai

        self.view = []  # this is a list of objects (food, and/or other creatures).
        self.sight = sight
        self.eye = eye

        # Energy consumptions
        self.basic_ec = basic_ec
        self.seeing_ec = seeing_ec
        self.speed_ec = speed_ec
        self.total_ec = self.basic_ec + self.seeing_ec + self.speed_ec
        self.energy = 100

    def otherUpdates(self, dt, **kwargs):
        ai_wrapper(self)  # This updates the speed
        # eye_wrapper(self, kwargs['creatures'], kwargs['foods'])  # this should become just the locations instead of
        # the whole things.

        self.seeing_ec = self.sight / 5e3
        self.speed_ec = self._velIntensity / 1e1
        self.total_ec = (self.basic_ec + self.seeing_ec + self.speed_ec) * dt

        self.energy -= self.total_ec

        if self.energy <= 0:
            self.die()
        print(self.energy)

    def _image_update(self):
        Thing._image_update(self)

        w = self.image.get_width()
        h = self.image.get_height()
        lifeRec = pygame.Rect((0, 0), (w, h / 10))
        lifeSubSurface = self.image.subsurface(lifeRec)
        lifeSubSurface.fill([100, 100, 100])

        lifeRecFull = pygame.Rect((0, 0), (w * self.energy / 100, h / 10))
        pygame.draw.rect(lifeSubSurface, [255, 0, 0], lifeRecFull, 0)
        # pygame.draw.circle(self.image.subsurface(, [100, 0, 0], (0, 0), 10)

    def eat(self, energy):
        self.energy += energy

    def die(self):
        self.kill()


class Creatures(Things):
    pass
