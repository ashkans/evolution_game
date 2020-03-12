import pygame
import math
from helper import getColor, getSurface


class Thing:
    def __init__(self, pos=None, speed=None, angle=None, size=None, color=None, imgName=None):
        if pos is None:
            pos = [10, 10]
        if speed is None:
            speed = [0, 0]
        if angle is None:
            angle = 0
        if size is None:
            size = 20
        if color is None:
            color = [100,255,255]
        if imgName is None:
            imgName = 'circle'

        self.pos = pos
        self.speed = speed
        self.angle = angle  # clockwise from top
        self.size = size
        self.color = color
        self.imgName = imgName

        self.img = getSurface(name=imgName, res=256, color=self.color).copy()

        self.visible = True
        self.id = 0

    def move(self, dt, boundaries):

        self.pos[0] += self.speed[0] * dt
        self.pos[1] += self.speed[1] * dt

        self.wall_check(boundaries['walls'])
        self.setAngleToSpeed()

    def setAngleToSpeed(self):
        if self.speed[0] != 0:
            self.angle = math.tan(self.speed[1] / self.speed[0])

    def draw(self, surface):
        if self.visible:
            s = pygame.transform.scale(self.img, (int(self.size), int(self.size)))
            pos = [self.pos[0] - self.size / 2, self.pos[1] - self.size / 2]
            surface.blit(s, pos)

    # TODO: This should be more general, including a set of boundaries such as polygon, and circle
    def wall_check(self, boundary):
        xmin = self.pos[0] - self.size / 2
        xmax = self.pos[0] + self.size / 2
        ymin = self.pos[1] - self.size / 2
        ymax = self.pos[1] + self.size / 2

        top = boundary[0]
        left = boundary[1]
        bottom = boundary[2]
        right = boundary[3]

        if xmax > right:
            c = xmax - right
            self.pos[0] -= 2 * c
            self.speed[0] *= -1
        elif xmin < left:
            c = xmin - left
            self.pos[0] -= 2 * c
            self.speed[0] *= -1

        if ymin < top:
            c = ymin - top
            self.pos[1] -= 2 * c
            self.speed[1] *= -1
        elif ymax > bottom:
            c = ymax - bottom
            self.pos[1] -= 2 * c
            self.speed[1] *= -1
