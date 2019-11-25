import math
import pygame
import numpy as np
from helper import check_eat


class Creature:
    def __init__(self, x=0, y=0, color=(255, 0, 0), size=10, shape=None):
        self.x = x
        self.y = y
        self.color = color

        self.azimut = math.pi / 2
        self.v = 1
        if shape is None:
            shape = 'circle'
        self.shape = shape
        self.size = size
        self.energy = 100

    def update(self):
        vx = self.v * math.sin(self.azimut)
        vy = self.v * math.cos(self.azimut)

        self.x += vx
        self.y += vy

        self.azimut += (np.random.random() - 0.5) * math.pi / 50
        self.azimut = math.fmod(self.azimut, 2 * math.pi)

        self.v += (np.random.random() - 0.5) / 100
        self.energy -= 0.05

    def draw(self, screen):

        if self.shape == 'rect':
            pygame.draw.rect(screen, self.color, (self.x - self.size, self.y - self.size, self.size * 2, self.size * 2))

        elif self.shape == 'circle':
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

        direction_x = int(self.x + self.size * math.sin(self.azimut) * 0.9)
        direction_y = int(self.y + self.size * math.cos(self.azimut) * 0.9)
        pygame.draw.circle(screen, (0, 0, 0), (direction_x, direction_y), int(self.size / 2))

        pygame.draw.rect(screen, (255, 255, 255),
                         (self.x - self.size, self.y - self.size * 1.4, self.size * 2, self.size * 0.3))
        pygame.draw.rect(screen, (255, 0, 0),
                         (self.x - self.size, self.y - self.size * 1.4, self.size * 2 * self.energy / 100,
                          self.size * 0.3))

    def boundary_check(self, right_x=None, left_x=None, top_y=None, bottom_y=None):
        xmin = self.x - self.size
        xmax = self.x + self.size
        ymin = self.y - self.size
        ymax = self.y + self.size

        if xmax > right_x:
            c = xmax - right_x
            self.x -= 2 * c
            self.azimut *= -1
        if xmin < left_x:
            c = xmin - left_x
            self.x -= 2 * c
            self.azimut *= -1
        if ymin < top_y:
            c = ymin - top_y
            self.y -= 2 * c
            self.azimut = math.pi / 2 - (self.azimut - math.pi / 2)
        if ymax > bottom_y:
            c = ymax - bottom_y
            self.y -= 2 * c
            self.azimut = math.pi / 2 - (self.azimut - math.pi / 2)

    def eat(self, energy):
        self.energy += energy


# TODO wrap all updates with a single update function.
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

    def update_pos(self):
        for creature in self.creatures:
            self.creatures[creature].update()

    def update_energy(self, foods):
        # check if any creature has eaten food.
        check_eat(self, foods)

        for food in foods.contents:
            for c in food.eaten_by:
                self.creatures[c].eat(food.energy_content / len(food.eaten_by))
        foods.remove_eaten()

    def draw(self, screen):
        for creature in self.creatures:
            self.creatures[creature].draw(screen)

    def boundary_check(self, **kwargs):
        for creature in self.creatures:
            self.creatures[creature].boundary_check(**kwargs)

    def update_death_and_born(self):
        to_be_del = []
        for c in self.creatures:
            if self.creatures[c].energy < 0:
                to_be_del.append(c)
        for c in to_be_del:
            del self.creatures[c]


class Food:
    def __init__(self, x=0, y=0, energy_content=10, color=(0, 0, 255), size=5):
        self.x = x
        self.y = y
        self.energy_content = energy_content
        self.color = color
        self.size = size
        self.blink = 0
        self.eaten_by = []

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x - self.size, self.y - self.size, self.size * 2, self.size * 2),
                         self.blink)


class Foods:
    def __init__(self):
        self.contents = []

    def draw(self, screen):
        for food in self.contents:
            food.draw(screen)

    def add_food(self, x=0, y=0, energy_content=10, color=(0, 0, 255), size=5):
        self.contents.append(Food(x, y, energy_content, color, size))
        print('food is added!')

    def update(self, width, height):
        # produce foodsP
        if len(self.contents) < 20:
            enough_food = False
            while not enough_food:
                self.add_food(x=width * np.random.random(), y=height * np.random.random())
                if len(self.contents) >= 20:
                    enough_food = True

    def remove_eaten(self):
        self.contents = [food for food in self.contents if len(food.eaten_by) == 0]
