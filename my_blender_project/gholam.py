import imp
from random import random, choice
import bobject
import numpy as np

# import pandas as pd

imp.reload(bobject)
from bobject import Bobject

# import helpers
from my_helpers import *

from my_helpers import apply_material


class Gholam(Bobject):
    def __init__(self, mat=None, **kwargs):
        objects = []
        bpy.ops.mesh.primitive_uv_sphere_add(size=.055, view_align=False, enter_editmode=False, location=(0, 0, .1))
        objects.append(bpy.context.active_object)
        bpy.ops.mesh.primitive_uv_sphere_add(size=.085, view_align=False, enter_editmode=False, location=(0, 0, 0))
        objects.append(bpy.context.active_object)
        bpy.ops.mesh.primitive_cone_add(radius1=1, radius2=0, depth=0.01, location=(0, 0, -0.025-0.025*random()))
        this_obj = bpy.context.active_object
        this_obj.show_transparent = True
        objects.append(this_obj)
        super().__init__(objects=objects, **kwargs)

        if mat is None:
            # mat = choice(bpy.data.materials.keys()[1:])
            mat = 'creature_color3'

        apply_material(self.ref_obj.children[1], mat)
        apply_material(self.ref_obj.children[2], mat)

        material = bpy.data.materials.new("mymaterial")
        material.diffuse_color = (0.6, 0.5, 0.5)

 #       obj.show_transparent = True  # displays trans in viewport


        apply_material(self.ref_obj.children[0], material)


    # mat ['clear', 'color1', 'color10', 'color2', 'color3', 'color4', 'color5', 'color6', 'color7', 'color8', 'color9',
    # 'creature_color1', 'creature_color10', 'creature_color2', 'creature_color3', 'creature_color4',
    # 'creature_color5', 'creature_color6', 'creature_color7', 'creature_color8', 'creature_color9', 'trans_color1',
    # 'trans_color10', 'trans_color2', 'trans_color3', 'trans_color4', 'trans_color5', 'trans_color6',
    # 'trans_color7', 'trans_color8', 'trans_color9']

    def from_log_file(self, file):
        my_data = np.genfromtxt(file, delimiter=',')
        st, x, y, e, sight = my_data[1][[1, 2, 3, 4, 5]]

        x = x * 6 - 3
        y = y * 6 - 3

        self.add_to_blender(appear_time=st, animate=True)
        self.move_to(0, 0, new_location=[x, y, 0.1], new_scale=e/200 + 0.5)



        for row in my_data[2:]:
            et, x, y, e, sight = row[[1, 2, 3, 4, 5]]

            x = x * 6 - 3
            y = y * 6 - 3
            self.move_to(start_time=st, end_time=et, new_location=[x, y, 0.1])
            self.sub_object_move_to(start_time=st, end_time=et, new_scale=e/200 + 0.5, child_ids=[1,2])
            self.sub_object_move_to(start_time=st, end_time=et, new_scale=sight/640, child_ids=[0])
            #self.ref_obj.children[0].scale = [1,1,1]#[1/s for s in self.intrinsic_scale]
            st = et
        self.disappear(disappear_time=et)

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


class Food(Bobject):
    def __init__(self, mat=None,  **kwargs):
        bpy.ops.mesh.primitive_cube_add(radius=.05, view_align=False, enter_editmode=False, location=(0, 0, 0))

        super().__init__(objects=[bpy.context.active_object], **kwargs)

        if mat is None:
            mat = 'color7'
        apply_material(self.ref_obj.children[0], mat)

    def from_single_log_file(self, my_data, id_tolook):

        my_data = my_data[my_data[:,1] == id_tolook, :]
        first_appearance = True
        for row in my_data:
            ID, t, x, y, energy_content = row[[1, 2, 3, 4, 5]]

            if ID == id_tolook:
                x = x * 6 - 3
                y = y * 6 - 3
                st = t
                if first_appearance:
                    self.add_to_blender(appear_time=st, animate=False, transition_time=0)
                    self.move_to(st-1, st-1, new_location=[x, y, 0.1])
                    first_appearance = False

                else:
                    self.move_to(start_time=st, end_time=et, new_location=[x, y, 0.1])
                et = st

        if not first_appearance:
            self.disappear(disappear_time=et, animate=False)
