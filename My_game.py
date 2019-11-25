# PyGame template.

# Import standard modules.
import sys
import numpy as np
# Import non-standard modules.
import pygame
from pygame.locals import *

# My libraries
from creature import Creature, Population, Foods


def update(dt, pop,foods, width, height):
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
    pop.update()
    foods.update(width,height)
    pop.boundary_check(right_x=width, left_x=0, top_y=0, bottom_y=height)


def draw(screen, pop,foods, width, height):
    """
    Draw things to the window. Called once per frame.
    """
    screen.fill((0, 100, 100))  # Fill the screen with black.

    pop.draw(screen)
    foods.draw(screen)
    # Flip the display so that the things we drew actually show up.
    pygame.display.flip()


def game_init(width, height):
    pop = Population()
    foods = Foods()


    for i in range(5):
        pop.add_creature(x=height * np.random.random(), y=width * np.random.random(), color=np.random.random(3) * 255,
                         size=10, shape='rect')
        pop.add_creature(x=height * np.random.random(), y=width * np.random.random(), color=np.random.random(3) * 255,
                         size=10, shape='circle')

    for i in range(5):
        foods.add_food(x=height * np.random.random(), y=width * np.random.random())


    return pop, foods

def runPyGame():

    # Initialise PyGame.
    pygame.init()
    #pygame.display.set_mode((1920, 1080))

    # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
    fps = 60.0
    fpsClock = pygame.time.Clock()

    # Set up the window.
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))

    # screen is the surface representing the window.
    # PyGame surfaces can be thought of as screen sections that you can draw onto.
    # You can also draw surfaces onto other surfaces, rotate surfaces, and transform surfaces.

    # Main game loop.
    dt = 1 / fps  # dt is the time since last frame.
    pop, foods = game_init(width, height)
    while True:  # Loop forever!
        update(dt, pop,foods, width, height)  # You can update/draw here, I've just moved the code for neatness.
        draw(screen, pop,foods, width, height)

        dt = fpsClock.tick(fps)


runPyGame()
