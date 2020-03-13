import pygame
import math
from helper import getColor, getSurface


class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()


class Thing(pygame.sprite.Sprite):

    def __init__(self, pos=None, speed=None, angle=None, size=None, color=None, imgName=None):
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

        self.pos = pos
        self.speed = speed
        self.angle = angle  # clockwise from top
        self.size = size
        self.color = color
        self.imgName = imgName

        # self.rect = pygame.Rect(pos, (size, size))
        self.origImage = getSurface(name=imgName, res=512, color=self.color).copy()
        self.image = self.origImage.copy()

        self.visible = True
        self.id = 0
        self.setAngleToSpeed()

    @property
    def rect(self):
        return self.image.get_rect(center=self.pos)

    def update(self, dt, boundaries):

        self.pos[0] += self.speed[0] * dt
        self.pos[1] += self.speed[1] * dt

        self.wall_check(boundaries['walls'])
        self.setAngleToSpeed()

        scale = self.size / self.origImage.get_width()
        self.image = pygame.transform.rotozoom(self.origImage, math.degrees(self.angle), scale)
        self.image.set_colorkey(self.origImage.get_colorkey())

    def rotate(self, sp, dt):
        self.angle += sp * dt

    def setAngleToSpeed(self):
        if self.speed[0] != 0:
            self.angle = -1 * math.atan(self.speed[1] / self.speed[0])
        if self.speed[0] < 0:
            self.angle += math.pi

    def draw(self, surface):
        surface.blit(self.image, self.rect)

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
