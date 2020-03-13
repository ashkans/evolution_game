import pygame


def check_eat(pop, foods):
    for c in pop.creatures:
        for food in foods.contents:
            if pop.creatures[c].x + pop.creatures[c].size > food.x - food.size:
                if pop.creatures[c].x - pop.creatures[c].size < food.x + food.size:
                    if pop.creatures[c].y + pop.creatures[c].size > food.y - food.size:
                        if pop.creatures[c].y - pop.creatures[c].size < food.y + food.size:
                            food.eaten_by.append(c)


def getSurface(name='circle', res=128, color=(50, 50, 50)):
    if isinstance(color, str):
        c = getColor(color)
    else:
        c = color

    if name == 'circle':
        s1d = 256
        surf1 = pygame.Surface((res, res))
        surf1.set_colorkey((0, 0, 0))
        pygame.draw.circle(surf1, c, (int(res / 2), int(res / 2)), int(res / 2))
        return surf1  # this should be a surface

    if name == 'bob':
        surf1 = pygame.Surface((res, res))
        #surf1.fill((255, 255, 255))
        surf1.set_colorkey((0, 0, 0))

        main_cricle_r = res / 2
        main_cricle_pos = (int(main_cricle_r), int(main_cricle_r))
        small_circle_r = res / 6
        small_circle_pos = (int(main_cricle_r*2- small_circle_r)), int(main_cricle_r)

        pygame.draw.circle(surf1, c, main_cricle_pos, int(main_cricle_r))
        pygame.draw.circle(surf1, (1, 1, 1), small_circle_pos, int(small_circle_r))
        return surf1  # this should be a surface


def getColor(c):
    if c == 'blue':
        rbg = (0, 0, 128)
    elif c == 'green':
        rbg = (0, 255, 0)
    elif c == 'white':
        rbg = (255, 255, 255)

    return rbg

