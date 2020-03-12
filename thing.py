import pygame
import math


class Thing:
    def __init__(self, pos=(0, 0), speed=(0, 0)):
        self.pos = [50, 50]
        self.speed = [0, 0]
        self.angle = 0  # clockwise from top
        self.size = 100
        self.color = [100, 255, 255]

        # TODO: this should be written more appropriatly.
        s1d = 256
        surf1 = pygame.Surface((s1d, s1d))
        surf1.set_colorkey((0, 0, 0))
        pygame.draw.circle(surf1, self.color, (int(s1d / 2), int(s1d / 2)), int(s1d / 2))
        self.img = surf1  # this should be a surface

        self.visible = True
        self.id = 0

    def move(self, dt):
        self.pos[0] += self.speed[0] * dt
        self.pos[1] += self.speed[1] * dt
        self.setAngleToSpeed()

    def setAngleToSpeed(self):
        self.angle = math.tan(self.speed[1] / self.speed[0])

    def draw(self, surface):
        if self.visible:
            s = pygame.transform.scale(self.img, (int(self.size), int(self.size)))
            surface.blit(s, self.pos)
