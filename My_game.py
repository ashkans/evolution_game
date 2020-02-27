# PyGame template.

# Import standard modules.
import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
from os.path import join
import os

matplotlib.use("Agg")

# Import non-standard modules.
import pygame
from pygame.locals import *

# My libraries
from creature import Creature, Population, Foods
from helper import check_eat

from Logger import Logger

import settings

SCALE = settings.SCALE
SPEED = settings.SPEED
DOMAIN_SCALE = settings.DOMAIN_SCALE
BASE_WIDTH = settings.BASE_WIDTH
BASE_HEIGHT = settings.BASE_HEIGHT

def update(t, dt, pop, foods, width, height):
    """
    Update game. Called once per frame.
    dt is the amount of time passed since last frame.
    If you want to have constant apparent movement no matter your framerate,
    what you can do is something like

    x += v * dt

    and this will scale your velocity based on time. Extend as necessary."""

    # Go through events that are passed to the script by the window.
    for event in pygame.event.get():
        # We need to handle these events. Initially the only one you'll want to care
        # about is the QUIT event, because if you don't handle it, your game will crash
        # whenever someone tries to exit.
        if event.type == QUIT:
            pygame.quit()  # Opposite of pygame.init
            sys.exit()  # Not including this line crashes the script on Windows. Possibly
            # on other operating systems too, but I don't know for sure.
        # Handle other events as you wish.

    # my updates:
    pop.update_pos(t, dt, foods)
    foods.update(t, dt, width, height)
    pop.boundary_check(right_x=width, left_x=0, top_y=0, bottom_y=height)

    pop.update_energy(t, dt, foods)
    pop.update_death_and_born(t)


def draw(screen, pop, foods, width, height):
    """
    Draw things to the window. Called once per frame.
    """
    screen.fill((150, 150, 150))  # Fill the screen with black.

    pop.draw(screen)
    foods.draw(screen)

    # Flip the display so that the things we drew actually show up.
    pygame.display.flip()


def draw_screen(screen, pop, foods, width, height):
    fig = plt.figure(figsize=[4, 4], dpi=100)
    plt.plot(np.random.random(10), np.random.random(10), '.')
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    surf = pygame.image.fromstring(raw_data, (400, 400), "RGB")
    screen.blit(surf, (0, 0))
    pygame.display.flip()


def game_init(width, height):
    pop = Population()
    foods = Foods()

    for i in range(5):
        pop.add_creature(x=width * np.random.random() / SCALE, y=height * np.random.random() / SCALE,
                         color=np.random.random(3) * 255,
                         size=10, shape='rect', eye='see_foods_loc', sight=100)

    for i in range(5):
        pop.add_creature(x=width * np.random.random() / SCALE, y=height * np.random.random() / SCALE,
                         color=np.random.random(3) * 255,
                         size=10, shape='circle', eye='see_foods_loc2', sight=25)
    for i in range(settings.INIT_FOODS):
        foods.add_food(x=width * np.random.random() / SCALE, y=height * np.random.random() / SCALE, t=0)

    return pop, foods


def game_exit(t, dt, pop, foods, width, height):

    if not os.path.exists(settings.LOG_FOLDER):
        os.makedirs(settings.LOG_FOLDER)
    # print(join(settings.LOG_FOLDER, 'food_log.csv'))
    pd.DataFrame(foods.history, columns=foods.history_list).to_csv(join(settings.LOG_FOLDER, 'food_log.csv'))

    pop.finalize(t)
    foods.finalize(t)


def runPyGame():
    # Initialise PyGame.
    pygame.init()

    # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
    fps = 60.0
    t = 0
    fpsClock = pygame.time.Clock()

    # Set up the window.

    width, height = int(BASE_WIDTH * SCALE * DOMAIN_SCALE), int(BASE_HEIGHT * SCALE * DOMAIN_SCALE)
    screen = pygame.display.set_mode((width, height))
    # plotting_screen = pygame.display.set_mode((width, height))

    # screen is the surface representing the window.
    # PyGame surfaces can be thought of as screen sections that you can draw onto.
    # You can also draw surfaces onto other surfaces, rotate surfaces, and transform surfaces.

    # Main game loop.
    dt = 1 / fps * SPEED  # dt is the time since last frame.

    pop, foods = game_init(width, height)
    while True:  # Loop forever!
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit(t, dt, pop, foods, width, height)
                pygame.quit()
                exit()

        update(t, dt, pop, foods, width, height)  # You can update/draw here, I've just moved the code for neatness.
        draw(screen, pop, foods, width, height)
        # draw_screen(screen, pop, foods, width, height)
        dt = fpsClock.tick(fps) * SPEED
        t += dt


runPyGame()
