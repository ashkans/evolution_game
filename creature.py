import math
import pygame
import numpy as np

from helper import check_eat
from creature_ai import ai_wrapper
from creature_eye import eye_wrapper

import settings

SCALE = settings.SCALE
SPEED = settings.SPEED


class Creature:
    def __init__(self, x=0, y=0, color=(255, 0, 0), size=10, shape=None, energy=100, azimuth=math.pi / 2,
                 eye='see_foods_loc', v=1, sight=0):
        self.x = x
        self.y = y
        self.color = color
        self.azimuth = azimuth
        self.v = v
        if shape is None:
            shape = 'circle'
        self.shape = shape
        self.size = size
        self.energy = energy
        self.ai = 'donkey'

        self.view = []  # this is a list of objects (food, and/or other creatures).
        self.sight = sight
        self.eye = eye

        # Energy consumptions
        self.basic_ec = 0
        self.seeing_ec = 0
        self.speed_ec = 0
        self.total_ec = self.basic_ec + self.seeing_ec + self.speed_ec

    def update(self, dt, pop, foods):  # for later food and pop should be changed to a shadow of these two object
        # with just
        # observable attributes!
        ai_wrapper(self)
        eye_wrapper(self, pop, foods)

        vx = self.v * dt / 30 * math.sin(self.azimuth)
        vy = self.v * dt / 30 * math.cos(self.azimuth)

        self.x += vx
        self.y += vy

        self.seeing_ec = self.sight / 5e3
        self.speed_ec = self.v / 1e2

        self.total_ec = (self.basic_ec + self.seeing_ec + self.speed_ec) * dt / 30
        self.energy -= self.total_ec

    def draw(self, screen):

        # this part can move to draw function of the population to reduce plotting burden, there all of the plotting
        # will be done in a single surface.
        # == Plotting the sight =========
        h = screen.get_height()
        w = screen.get_width()
        s = pygame.Surface((w, h), pygame.SRCALPHA)  # per-pixel alpha
        pygame.draw.circle(s, (255, 255, 255, 20), (int(self.x * SCALE), int(self.y * SCALE)), int(self.sight * SCALE))
        screen.blit(s, (0, 0))
        # ===============================

        if self.shape == 'rect':
            pygame.draw.rect(screen, self.color,
                             ((self.x - self.size) * SCALE, (self.y - self.size) * SCALE,
                              self.size * 2 * SCALE, self.size * 2 * SCALE))

        elif self.shape == 'circle':
            pygame.draw.circle(screen, self.color, (int(self.x * SCALE), int(self.y * SCALE)), int(self.size * SCALE))

        direction_x = int((self.x + self.size * math.sin(self.azimuth) * 0.9) * SCALE)
        direction_y = int((self.y + self.size * math.cos(self.azimuth) * 0.9) * SCALE)
        pygame.draw.circle(screen, (0, 0, 0), (direction_x, direction_y), int(self.size / 2 * SCALE))

        pygame.draw.rect(screen, (255, 255, 255),
                         ((self.x - self.size) * SCALE, (self.y - self.size * 1.4) * SCALE, self.size * 2 * SCALE,
                          self.size * 0.3 * SCALE))
        pygame.draw.rect(screen, (255, 0, 0),
                         ((self.x - self.size) * SCALE, (self.y - self.size * 1.4) * SCALE,
                          self.size * 2 * self.energy / 100 * SCALE,
                          self.size * 0.3 * SCALE))

        # draw sight
        # draw sight

    def boundary_check(self, right_x=None, left_x=None, top_y=None, bottom_y=None):
        xmin = self.x - self.size
        xmax = self.x + self.size
        ymin = self.y - self.size
        ymax = self.y + self.size

        right_x /= SCALE
        left_x /= SCALE
        top_y /= SCALE
        bottom_y /= SCALE

        if xmax > right_x:
            c = xmax - right_x
            self.x -= 2 * c
            self.azimuth *= -1
        if xmin < left_x:
            c = xmin - left_x
            self.x -= 2 * c
            self.azimuth *= -1
        if ymin < top_y:
            c = ymin - top_y
            self.y -= 2 * c
            self.azimuth = math.pi / 2 - (self.azimuth - math.pi / 2)
        if ymax > bottom_y:
            c = ymax - bottom_y
            self.y -= 2 * c
            self.azimuth = math.pi / 2 - (self.azimuth - math.pi / 2)

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

    def regenerate_monosexual(self, creature, full_name):  # TODO This should be moved to a new py file
        sight = max(creature.sight + (np.random.random() - 0.5) * 20, 0)
        self.add_creature(full_name, x=creature.x, y=creature.y, color=creature.color, shape=creature.shape,
                          size=creature.size, energy=50, azimuth=np.random.random() * 2 * math.pi, eye=creature.eye,
                          v=creature.v, sight=sight)

    def update_pos(self, dt, foods):
        for creature in self.creatures:
            self.creatures[creature].update(dt, self, foods)

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
        to_regenerate = []
        for c in self.creatures:
            if self.creatures[c].energy < 0:
                to_be_del.append(c)
            elif self.creatures[c].energy > 100:
                self.creatures[c].energy = 50
                to_regenerate.append(c)

        for c in to_be_del:
            del self.creatures[c]

        for c in to_regenerate:
            self.regenerate_monosexual(self.creatures[c], c)

        # Born


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
        pygame.draw.rect(screen, self.color, ((self.x - self.size) * SCALE, (self.y - self.size) * SCALE,
                                              self.size * 2 * SCALE, self.size * 2 * SCALE), self.blink)


class Foods:
    def __init__(self):
        self.contents = []
        self.time_from_last_production = 0

    def draw(self, screen):
        for food in self.contents:
            food.draw(screen)

    def add_food(self, x=0, y=0, energy_content=10, color=(0, 0, 255), size=5):
        self.contents.append(Food(x, y, energy_content, color, size))
        print('food is added!')

    def update(self, dt, width, height):
        self.time_from_last_production += dt
        # produce foodsP
        if self.time_from_last_production > 500:
            self.time_from_last_production -= 500
            self.add_food(x=width * np.random.random() / SCALE, y=height * np.random.random() / SCALE)

        # if len(self.contents) < 20:
        #     enough_food = False
        #     while not enough_food:
        #         self.add_food(x=width * np.random.random() / SCALE, y=height * np.random.random() / SCALE)
        #         if len(self.contents) >= 20:
        #             enough_food = True

    def remove_eaten(self):
        self.contents = [food for food in self.contents if len(food.eaten_by) == 0]
