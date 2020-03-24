from thing import Thing, Things
from random import random
from creature_ai import ai_wrapper
from creature_eye import eye_wrapper
import pygame
from random import randint
from copy import deepcopy


class Creature(Thing):

    def __init__(self, energy=None, ai=None, sight=None, eye=None, basic_ec=None, seeing_ec=None, speed_ec=None,
                 **kwargs):

        if 'imgName' not in kwargs.keys():
            kwargs['imgName'] = 'bob'
        Thing.__init__(self, **kwargs)

        if ai is None:
            ai = 'donkey'
        if sight is None:
            sight = 0

        if eye is None:
            eye = 'see_foods_loc'

        if basic_ec is None:
            basic_ec = 0

        self.energy = energy
        self.ai = ai

        self.view = []  # this is a list of objects (food, and/or other creatures).
        self.sight = sight
        self.eye = eye

        # Energy consumptions
        self.basic_ec = basic_ec

        self.energy = 100

    @property
    def intSight(self):
        return int(self.sight)

    def eat(self, energy):
        self.energy += energy

    def die(self):
        self.kill()

    def otherUpdates(self, dt, **kwargs):
        ai_wrapper(self)  # This updates the speed
        eye_wrapper(self, kwargs['creatures'], kwargs['foods'])  # this should become just the locations instead of
        # the whole things.

        self.energy -= self.total_ec * dt

        if self.energy <= 0:
            self.die()
        elif self.energy > 100:
            self.regenerateMonosexual()
            self.energy = 50

    @property
    def seeing_ec(self):
        return self.sight / 5e4

    @property
    def speed_ec(self):
        return self._velIntensity ** 2 * 5


    @property
    def total_ec(self):
        return self.basic_ec + self.seeing_ec + self.speed_ec

    def image_update(self, zoom):
        Thing.image_update(self, zoom)

        w = self.image.get_width()
        h = self.image.get_height()
        lifeRec = pygame.Rect((0, 0), (w, h / 10))
        lifeSubSurface = self.image.subsurface(lifeRec)

        lifeSubSurface.fill([100, 100, 100])

        lifeRecFull = pygame.Rect((0, 0), (w * self.energy / 100, h / 10))
        pygame.draw.rect(lifeSubSurface, [255, 0, 0], lifeRecFull, 0)

        # pygame.draw.circle(self.image.subsurface(, [100, 0, 0], (0, 0), 10)

    def regenerateMonosexual(self):  # TODO This should be moved to a new py file
        group = self.groups()[0]

        offSpring = Creature(color=self.color, size=self.size)

        # TODO should set with a get/set routin in the creature class which consist of the gens.
        offSpring.pos = self.pos.copy()
        offSpring.speed = self.speed.copy()
        offSpring.imgName = self.imgName
        offSpring.sight = max(self.sight + (random() - 0.5) / 0.1, 3)

        offSpring.energy = 50
        offSpring.speed[0] += (random() - 0.5) / 10
        offSpring.speed[1] += (random() - 0.5) / 10

        # mutation

        group.add(offSpring)


class Creatures(Things):
    def check_eat(self, foods):
        collide_dict = pygame.sprite.groupcollide(foods, self, False, False, pygame.sprite.collide_circle_ratio(0.7))
        for food, creature_who_eat in collide_dict.items():
            food.eaten_by = creature_who_eat

    def drawSights(self, surface, currentViewSprite):
        # draw sights
        visibleSprites = pygame.sprite.spritecollide(currentViewSprite, self, False)

        W = surface.get_width()
        H = surface.get_height()

        w = currentViewSprite.rect.width
        h = currentViewSprite.rect.height

        wr = w / W
        hr = h / H

        for spr in visibleSprites:
            size = (spr.intSight * 2 / hr, spr.intSight * 2 / wr)
            R = int(spr.intSight / hr)
            s = pygame.Surface(size, pygame.SRCALPHA)  # per-pixel alpha

            pygame.draw.circle(s, [0, 0, 0, 10], [R, R], R, 0)

            rect = pygame.Rect((0, 0), size)
            rect.center = spr.rect.center

            currentViewRect = pygame.Rect(currentViewSprite)
            rect.center = ((rect.centerx - currentViewRect.top) / hr, (rect.centery - currentViewRect.left) / wr)
            surface.blit(s, rect)
