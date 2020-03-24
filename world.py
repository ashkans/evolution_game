import pygame
from os.path import join
from random import randint
from creature import Creature, Population, Foods
import numpy as np
from thing import Thing, Things
from helper import getColor
from food import Food, Foods
from creatureRefactor import Creature, Creatures
from config import SETTING


class World:
    def __init__(self, setting=None):
        self.background = (255, 255, 255)  # _get_rand_color()
        if setting is None:
            from config import SETTING as setting

        # read in attrbiutes from config
        #        for key in setting:
        #            setattr(self, key, setting[key])

        # Initialise PyGame.
        pygame.init()

        # the quit function
        # pygame.register_qui()

        # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
        self.currentZoomCenter = (300, 300)
        self.currentZoom = 1

        self.wordRect = pygame.Rect(0, 0, SETTING['WORLD']['HEIGHT'], SETTING['WORLD']['WIDTH'])
        self.t = 0
        self.dt = 0
        self.boundaries = {
            'walls': [self.wordRect.top, self.wordRect.left, self.wordRect.bottom, self.wordRect.right]}
        self.things = Things()
        self.foods = Foods()
        self.creatures = Creatures()

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

        for i in range(1):
            self.creatures.add(
                Creature(speed=[randint(-30, 30) / 500, randint(-30, 30) / 500], size=10, imgName='bob',
                         color=[255, 155, 0],
                         pos=[randint(1, SETTING['WORLD']['HEIGHT']), randint(1, SETTING['WORLD']['WIDTH'])],
                         sight=50))

        for i in range(SETTING['FOOD']['APPLE']['INIT']):
            self.foods.add(
                Food(imgName='apple', still=True, size=SETTING['FOOD']['APPLE']['SIZE'],
                     color=[randint(1, 255), randint(1, 255), randint(1, 255)],
                     pos=[randint(1, SETTING['WORLD']['HEIGHT']), randint(1, SETTING['WORLD']['WIDTH'])]))

            # pos=[randint(1, SETTING['WORLD']['HEIGHT']), randint(1, SETTING['WORLD']['WIDTH'])]

        # self.things.append(Thing(speed=[0.18, 0.06], size=50, imgName='bob', pos=[randint(0,100), randint(0,100)]))

        # self.blocks = pygame.sprite.Group()
        # self.blocks.add(b)

    def _setup_window(self):
        # width, height = int(self.DISPLAY['WIDTH']), int(self.DISPLAY['HEIGHT'])
        self.window = pygame.display.set_mode((int(SETTING['DISPLAY']['WINDOW_RES']['WIDTH']),
                                               int(SETTING['DISPLAY']['WINDOW_RES']['HEIGHT'])))

    def _get_main_screen(self):
        return pygame.Surface(
            (int(SETTING['DISPLAY']['MAIN_SCREEN_RES']['WIDTH']), int(SETTING['DISPLAY']['MAIN_SCREEN_RES']['HEIGHT'])))

    def _get_details_screen(self):
        return pygame.Surface(
            (int(SETTING['DISPLAY']['DETAILS_SCREEN_RES']['WIDTH']),
             int(SETTING['DISPLAY']['DETAILS_SCREEN_RES']['HEIGHT'])))

    def update(self):

        for creature in self.creatures:
            creature.update(dt=self.dt, boundaries=self.boundaries, foods=self.foods, creatures=self.creatures)

        for food in self.foods:
            food.update(dt=self.dt, boundaries=self.boundaries)

        self.creatures.check_eat(self.foods)
        self.foods.add_food(self.dt)
        '''
        self.things[0].move(dt=1, boundaries=self.boundries)
        self.things[1].move(dt=1, boundaries=self.boundries)
'''

    def draw(self):

        self.surfaces['main'].fill(self.background)
        origin = (int(SETTING['DISPLAY']['MAIN_SCREEN_RES']['LEFT']), int(SETTING['DISPLAY']['MAIN_SCREEN_RES']['TOP']))
        # self.pop.draw(self.surfaces['main'])
        # self.foods.draw(self.surfaces['main'])

        # TODO tidy up!
        self.currentView = pygame.Rect(0, 0, int(SETTING['DISPLAY']['MAIN_SCREEN_RES']['WIDTH'] / self.currentZoom),
                                       int(SETTING['DISPLAY']['MAIN_SCREEN_RES']['HEIGHT']) / self.currentZoom)
        self.currectViewSprite = pygame.sprite.Sprite()
        self.currectViewSprite.rect = self.currentView
        # ===============================
        self.foods.draw(self.surfaces['main'], self.currectViewSprite)
        self.creatures.draw(self.surfaces['main'], self.currectViewSprite)

        self.creatures.drawSights(self.surfaces['main'], self.currectViewSprite)
        # self.things.sprites()[0].draw(self.surfaces['main'])

        # ===============================
        '''
        size = self.surfaces['main'].get_size()
        newSize = [int(size[0] * self.currentZoom), int(size[1] * self.currentZoom)]

        s = pygame.transform.scale(self.surfaces['main'], newSize)
        self.surfaces['main'].fill([50, 50, 50])
        self.surfaces['main'].blit(s, [0, 0])
        '''
        self.window.blit(self.surfaces['main'], origin)

        self.surfaces['details'].fill(getColor('green'))  # TODO the backgrounds should be separated
        origin = (
            int(SETTING['DISPLAY']['DETAILS_SCREEN_RES']['LEFT']), int(SETTING['DISPLAY']['DETAILS_SCREEN_RES']['TOP']))
        if 'mousePos' in self.texts.keys():
            self.surfaces['details'].blit(*self.texts['mousePos'])

        for _, t in self.texts.items():
            self.surfaces['details'].blit(*t)

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
                    self.currentZoomCenter = event.pos

                if event.button == 4:
                    textPos = (10, 30)
                    self.currentZoom += 0.1
                    self.texts['zoom'] = self.createText('%4.2f' % self.currentZoom, textPos)

                    # self.background = _transform_color(self.background, 1.05)

                if event.button == 5:
                    textPos = (10, 30)
                    self.currentZoom -= 0.1
                    self.currentZoom = max(self.currentZoom, 0.1)
                    self.texts['zoom'] = self.createText('%4.2f' % self.currentZoom, textPos)
                    # self.background = _transform_color(self.background, 0.95)

    def _get_dt(self):
        postprocessing = False
        if postprocessing:
            self.dt = 1000 / self.DISPLAY['FPS']  # * SPEED
            # pygame.image.save(self.surface, join(self.LOGGER['FOLDER'], "screenshot%d.JPEG" % self.frameCount))
        else:
            self.dt = self.fpsClock.tick(SETTING['DISPLAY']['FPS'])  # * SPEED

    def run(self):
        while True:  # Loop forever!

            self._check_events()

            self.frameCount += 1

            self.update()
            self.draw()

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
