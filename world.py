import pygame
from os.path import join
from random import randint
from creature import Creature, Population, Foods
import numpy as np
from thing import Thing, Things
from helper import getColor
from food import Food, Foods


class World:
    def __init__(self, setting=None):
        self.background = (255, 255, 255)  # _get_rand_color()
        if setting is None:
            from config import SETTING as setting

        # read in attrbiutes from config
        for key in setting:
            setattr(self, key, setting[key])

        # Initialise PyGame.
        pygame.init()

        # the quit function
        # pygame.register_qui()

        # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
        self.t = 0
        self.dt = 0
        self.boundries = {
            'walls': [0, 0, self.DISPLAY['MAIN_SCREEN_RES']['HEIGHT'], self.DISPLAY['MAIN_SCREEN_RES']['WIDTH']]}
        self.things = Things()
        self.foods = Foods()
        self._gameInit()

        self.frameCount = 0

        self.fpsClock = pygame.time.Clock()

        # Set up the window.
        self._setup_window()

        self.surfaces = {'main': self._get_main_screen(), 'details': self._get_details_screen()}
        self.texts = {}

        self.update()

        self.draw()

    def _gameInit(self):
        w, h = (int(self.DISPLAY['MAIN_SCREEN_RES']['WIDTH']), int(self.DISPLAY['MAIN_SCREEN_RES']['HEIGHT']))

        for i in range(300):
            self.things.add(Thing(speed=[randint(5, 30)/100, randint(5, 30)/100], size=randint(30, 50), imgName='bob',
                                  color=[randint(1, 255), randint(1, 255), randint(1, 255)],
                                  pos=[randint(1, 200), randint(1, 200)]))

            self.foods.add(Food(imgName= 'apple', still=True, size=60, color=[randint(1, 255), randint(1, 255), randint(1, 255)],
                                pos=[randint(1, 600), randint(1, 600)]))


        # self.things.append(Thing(speed=[0.18, 0.06], size=50, imgName='bob', pos=[randint(0,100), randint(0,100)]))

        # self.blocks = pygame.sprite.Group()
        # self.blocks.add(b)

    def _setup_window(self):
        # width, height = int(self.DISPLAY['WIDTH']), int(self.DISPLAY['HEIGHT'])
        self.window = pygame.display.set_mode((int(self.DISPLAY['WINDOW_RES']['WIDTH']),
                                               int(self.DISPLAY['WINDOW_RES']['HEIGHT'])))

    def _get_main_screen(self):
        return pygame.Surface(
            (int(self.DISPLAY['MAIN_SCREEN_RES']['WIDTH']), int(self.DISPLAY['MAIN_SCREEN_RES']['HEIGHT'])))

    def _get_details_screen(self):
        return pygame.Surface(
            (int(self.DISPLAY['DETAILS_SCREEN_RES']['WIDTH']), int(self.DISPLAY['DETAILS_SCREEN_RES']['HEIGHT'])))

    def update(self):

        for thing in self.things:
            thing.update(dt=self.dt, boundaries=self.boundries)

        for food in self.foods:
            food.update(dt=self.dt, boundaries=self.boundries)
        '''
        self.things[0].move(dt=1, boundaries=self.boundries)
        self.things[1].move(dt=1, boundaries=self.boundries)
'''

    def draw(self):

        self.surfaces['main'].fill(self.background)
        origin = (int(self.DISPLAY['MAIN_SCREEN_RES']['LEFT']), int(self.DISPLAY['MAIN_SCREEN_RES']['TOP']))
        # self.pop.draw(self.surfaces['main'])
        # self.foods.draw(self.surfaces['main'])

        # ===============================
        self.foods.draw(self.surfaces['main'])
        self.things.draw(self.surfaces['main'])
        # self.things.sprites()[0].draw(self.surfaces['main'])


        # ===============================

        self.window.blit(self.surfaces['main'], origin)

        self.surfaces['details'].fill(getColor('green'))  # TODO the backgrounds should be separated
        origin = (int(self.DISPLAY['DETAILS_SCREEN_RES']['LEFT']), int(self.DISPLAY['DETAILS_SCREEN_RES']['TOP']))
        if 'mousePos' in self.texts.keys():
            self.surfaces['details'].blit(*self.texts['mousePos'])

        self.window.blit(self.surfaces['details'], origin)

        pygame.display.flip()

    def exit(self):
        pygame.quit()
        exit()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.background = _get_rand_color()
                    textPos = (10, 10)
                    self.texts['mousePos'] = self.createText(str(event.pos), textPos)

                if event.button == 4:
                    self.background = _transform_color(self.background, 1.05)

                if event.button == 5:
                    self.background = _transform_color(self.background, 0.95)

    def _get_dt(self):
        postprocessing = False
        if postprocessing:
            self.dt = 1000 / self.DISPLAY['FPS']  # * SPEED
            # pygame.image.save(self.surface, join(self.LOGGER['FOLDER'], "screenshot%d.JPEG" % self.frameCount))
        else:
            self.dt = self.fpsClock.tick(self.DISPLAY['FPS'])  # * SPEED

    def run(self):
        while True:  # Loop forever!

            self._check_events()

            self.frameCount += 1

            self.update()  # You can update/draw here, I've just moved the code for neatness.
            self.draw()
            # draw_screen(screen, pop, foods, width, height)
            self._get_dt()

            self.t += self.dt

    def createText(self, text, location):
        # create a font object.
        # 1st parameter is the font file
        # which is present in pygame.
        # 2nd parameter is size of the font
        font = pygame.font.Font('freesansbold.ttf', 16)

        # create a text suface object,
        # on which text is drawn on it.
        renderedText = font.render(text, True, getColor('green'), getColor('blue'))

        # create a rectangular object for the
        # text surface object
        textRect = renderedText.get_rect()

        # set the center of the rectangular object.

        textRect.topleft = (location[0], location[1])

        return renderedText, textRect


def _get_rand_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)


def _transform_color(c, factor):
    r = min(max(c[0] * factor, 0), 255)
    b = min(max(c[1] * factor, 0), 255)
    g = min(max(c[2] * factor, 0), 255)
    c = (r, b, g)
    return c
