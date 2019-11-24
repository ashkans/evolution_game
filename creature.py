import math
import pygame
import numpy as np


class Creature:
    def __init__(self, x=0, y=0, color=(255, 0, 0), size=10):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.azimut = math.pi
        self.v = 1

    def update(self):
        vx = self.v * math.sin(self.azimut)
        vy = self.v * math.cos(self.azimut)

        self.x += vx
        self.y += vy

        self.azimut += (np.random.random() - 0.5) * math.pi / 5
        self.azimut = math.fmod(self.azimut, 2 * math.pi)

        self.v += (np.random.random() - 0.5) / 10

    def boundary_check(self, right_x=None, left_x=None, top_y=None, bottom_y=None):
        x = self.x
        y = self.y
        size = self.size
        if x + size / 2 > right_x:
            self.x = 2 * right_x - x - size
            self.azimut *= -1
        if x - size / 2 < left_x:
            self.x = 2 * left_x - (x - size)
            self.azimut *= -1
        if y - size / 2 < top_y:
            self.y = 2 * top_y - (y - size)
            self.azimut = math.pi / 2 - (self.azimut - math.pi / 2)
        if y + size / 2 > bottom_y:
            self.y = 2 * bottom_y - (y + size)
            self.azimut = math.pi / 2 - (self.azimut - math.pi / 2)


class Population:
    def __init__(self):
        self.creatures = {}

    def add_creature(self, full_name='C', **kwargs):

        while full_name in self.creatures.keys():
            split_name = full_name.split('_')
            try:
                split_name[-1] = str(float(split_name[-1]) + 1)
            except:
                split_name.append(str(0))

            full_name = '_'.join(split_name)

        self.creatures[full_name] = Creature(**kwargs)

    def update(self):
        for creature in self.creatures:
            self.creatures[creature].update()

    def draw(self, screen):
        for creature in self.creatures:
            # Redraw screen here.
            c = self.creatures[creature]
            pygame.draw.rect(screen, c.color, (c.x - c.size / 4, c.y - c.size / 4, c.size, c.size))

    def boundary_check(self, **kwargs):
        for creature in self.creatures:
            self.creatures[creature].boundary_check(**kwargs)
