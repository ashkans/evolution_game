###########################################################
import sys
import os
import importlib
import bpy

BASE_PATH = r"C:\Users\ashka\Documents\git\evolution_game"
BASE_PATH_blender = os.path.join(BASE_PATH, "my_blender_project")
sys.path.append(BASE_PATH_blender)

import settings
import numpy as np
importlib.reload(settings)
from settings import DEFAULT_SCENE_DURATION

import my_helpers
import math

importlib.reload(my_helpers)
from my_helpers import initialize_blender, cam_and_swivel, link_descendants, apply_material


import bobject
importlib.reload(bobject)
from bobject import Bobject

import gholam
importlib.reload(gholam)
from gholam import Gholam, Food


# from blobject import Blobject
###########################################################

cam_x = -7
cam_y = 7
cam_ang = math.atan(-1 * cam_x / cam_y) - 0.05

initialize_blender(total_duration=538)
cam_bobj, cam_swivel = cam_and_swivel(
    cam_location=[0, cam_x, cam_y],
    cam_rotation_euler=[cam_ang, 0, 0],
    cam_name="Camera Bobject",
    swivel_location=[0, 0, 0],
    swivel_rotation_euler=[0, 0, 0],
    swivel_name='Cam swivel',
    # control_sun = True
)
cam_swivel.add_to_blender(appear_time=-1, animate=False)
#cam_swivel.move_to(0,6,new_angle=[0,0,1])

# Make floor
bpy.ops.mesh.primitive_plane_add(radius=3, view_align=False, enter_editmode=False, location=(0, 0, 0))
floor = bpy.context.active_object
floor_Bobject = Bobject(objects=[floor])
#floor.color_shift()
floor_Bobject.add_to_blender(appear_time=-1, animate=False)
apply_material(floor_Bobject.ref_obj.children[0], 'color2')


log_folder = os.path.join(BASE_PATH, 'log_files')

koonderazan = []
for i in range(52): #52
    print(i)
    koonderazan.append(Gholam())
    koonderazan[-1].from_log_file(os.path.join(log_folder, '%d_log.csv' % i))

foods = []
file = os.path.join(log_folder, 'food_log.csv')
my_data = np.genfromtxt(file, delimiter=',')
for i in range(2173): # 2173
    print(i)
    foods.append(Food())
    foods[-1].from_single_log_file(my_data, i)
