import imp
from random import random, choice
import bobject
import numpy as np

imp.reload(bobject)
from bobject import Bobject

# import helpers
from my_helpers import *

from my_helpers import apply_material


class Gholam(Bobject):
    def __init__(self, mat=None, **kwargs):
        bpy.ops.mesh.primitive_cube_add(radius=.1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(
            True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False,
            False, False, False, False))
        super().__init__(objects=[bpy.context.active_object], **kwargs)

        if mat is None:
            mat = choice(bpy.data.materials.keys()[1:])
        apply_material(self.ref_obj.children[0], mat)

    # mat ['clear', 'color1', 'color10', 'color2', 'color3', 'color4', 'color5', 'color6', 'color7', 'color8', 'color9',
    # 'creature_color1', 'creature_color10', 'creature_color2', 'creature_color3', 'creature_color4',
    # 'creature_color5', 'creature_color6', 'creature_color7', 'creature_color8', 'creature_color9', 'trans_color1',
    # 'trans_color10', 'trans_color2', 'trans_color3', 'trans_color4', 'trans_color5', 'trans_color6',
    # 'trans_color7', 'trans_color8', 'trans_color9']

    def gol_gasht(self, bounciness=None):

        x = 0
        y = 0
        vx = random() - 0.5
        vy = random() - 0.2
        ax = 0
        ay = -0.01
        z = 0.1

        bounciness = random() * 0.2 + 0.8 if bounciness is None else bounciness

        self.move_to(0, 0, new_location=[x * 10, y * 10, z])
        for from_time in range(60 * 60):

            x += vx / 10
            y += vy / 10

            vx += ax
            vy += ay

            ax += (random() - 0.5) / 20000

            if np.abs(x) > 3:
                x = np.sign(x) * (3 - (np.abs(x) - 3) * 0.005)
                vx *= -0.9 * bounciness

            if np.abs(y) > 3:
                y = np.sign(y) * (3 - (np.abs(y) - 3) * 0.005)
                vy *= -0.8 * bounciness

            if from_time == 1000:
                vy += 1.5

            self.move_to(from_time / 60, (from_time + 1) / 60, new_location=[x, y, z])
