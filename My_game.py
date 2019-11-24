# PyGame template.

# Import standard modules.
import sys
import numpy as np
# Import non-standard modules.
import pygame
from pygame.locals import *

# My libraries
from creature import Creature, Population


def update(dt, pop, width, height):
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
    pop.boundary_check(right_x=width-100, left_x=10, top_y=10, bottom_y=height-100)


def draw(screen, pop, width, height):
    """
    Draw things to the window. Called once per frame.
    """
    screen.fill((0, 100, 100))  # Fill the screen with black.

    s = pygame.Surface((width - 100, height - 100))  # the size of your rect
    s.set_alpha(128)  # alpha level
    s.fill((255, 255, 255))  # this fills the entire surface
    screen.blit(s, (10, 10))  # (0,0) are the top-left coordinates

    pop.draw(screen)
    # Flip the display so that the things we drew actually show up.
    pygame.display.flip()


def game_init(width, height):
    pop = Population()

    for i in range(20):
        pop.add_creature(x=width * np.random.random(), y=height * np.random.random(), color=np.random.random(3) * 255, size = 30)

    return pop


def runPyGame():
    # Initialise PyGame.
    pygame.init()

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
    pop = game_init(width, height)
    while True:  # Loop forever!
        update(dt, pop, width, height)  # You can update/draw here, I've just moved the code for neatness.
        draw(screen, pop, width, height)

        dt = fpsClock.tick(fps)


runPyGame()
