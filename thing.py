import pygame
import math
from helper import getColor, getSurface
from random import random


class Thing(pygame.sprite.Sprite):

    def __init__(self, pos=None, speed=None, angle=None, size=None, color=None, imgName=None, still=None,
                 rotationRate=None):
        pygame.sprite.Sprite.__init__(self)

        if pos is None:
            pos = [10, 10]
        if speed is None:
            speed = [0, 0]
        if angle is None:
            angle = 0
        if size is None:
            size = 20
        if color is None:
            color = [100, 255, 255]
        if imgName is None:
            imgName = 'circle'
        if still is None:
            still = False
        if rotationRate is None:
            rotationRate = 0.0005

        self.pos = pos
        self.speed = speed
        self.angle = angle  # clockwise from top
        self.size = size
        self.color = color
        self.imgName = imgName
        self.still = still
        self.rotationRate = rotationRate

        # self.rect = pygame.Rect(pos, (size, size))
        self.origImage = getSurface(name=imgName, res=32, color=self.color).copy()

        scale = self.size / self.origImage.get_width()
        self.image = pygame.transform.rotozoom(self.origImage, math.degrees(self.angle), scale)
        self.image.set_colorkey(self.origImage.get_colorkey())

        self.id = 0

        if not self.still:
            self.setAngleToSpeed()

    @property
    def rect(self):
        return self.image.get_rect(center=self.pos)

    def update(self, dt, boundaries, **kwargs):
        if not self.still:
            self._move(dt, boundaries)
        self._image_update()
        self.otherUpdates(dt, **kwargs)

    def otherUpdates(self, dt):
        pass

    @property
    def _velIntensity(self):
        return (self.speed[0] ** 2 + self.speed[1] ** 2) ** 0.5

    @property
    def _velAngle(self):
        if self.speed[0] != 0:
            ang = math.atan(self.speed[1] / self.speed[0])
        else:
            ang = 0
        if self.speed[0] < 0:
            ang += math.pi

        return ang

    def _move(self, dt, boundaries):
        # movement
        self.pos[0] += self.speed[0] * dt
        self.pos[1] += self.speed[1] * dt

        if not self.still:
            self.wall_check(boundaries['walls'])
            self.setAngleToSpeed()

    def _image_update(self):
        # image update
        scale = self.size / self.origImage.get_width()
        self.image = pygame.transform.rotozoom(self.origImage, math.degrees(self.angle), scale)
        self.image.set_colorkey(self.origImage.get_colorkey())

    def rotate(self, sp=None, dt=0):
        if sp is None:
            sp = self.rotationRate
        self.angle += sp * dt

    def setAngleToSpeed(self):
        if self.speed[0] != 0:
            self.angle = -1 * math.atan(self.speed[1] / self.speed[0])
        if self.speed[0] < 0:
            self.angle += math.pi

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


class Things(pygame.sprite.Group):
    pass
