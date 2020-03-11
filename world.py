import pygame
from os.path import join
from random import randint


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
        self.pop = None
        self.foods = None
        self.frameCount = 0
        self.fpsClock = pygame.time.Clock()

        # Set up the window.
        self._setup_window()
        self._setup_main_screen()

        self.update()
        self.draw()

    def _setup_window(self):
        # width, height = int(self.DISPLAY['WIDTH']), int(self.DISPLAY['HEIGHT'])
        self.window = pygame.display.set_mode((int(self.DISPLAY['WINDOW_RES']['WIDTH']),
                                               int(self.DISPLAY['WINDOW_RES']['HEIGHT'])))

    def _setup_main_screen(self):
        self.surface = pygame.Surface(
            (int(self.DISPLAY['SCREEN_RES']['WIDTH']), int(self.DISPLAY['SCREEN_RES']['HEIGHT'])))

    def update(self):
        pass

    def draw(self):

        self.surface.fill(self.background)

        origin = (int(self.DISPLAY['SCREEN_RES']['LEFT']), int(self.DISPLAY['SCREEN_RES']['TOP']))
        self.window.blit(self.surface, origin)

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


def _get_rand_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)


def _transform_color(c, factor):
    r = min(max(c[0] * factor, 0), 255)
    b = min(max(c[1] * factor, 0), 255)
    g = min(max(c[2] * factor, 0), 255)
    c = (r, b, g)
    return c
