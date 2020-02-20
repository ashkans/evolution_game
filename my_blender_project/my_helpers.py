from settings import DEFAULT_SCENE_DURATION, SAMPLE_COUNT, LIGHT_SAMPLING_THRESHOLD, RESOLUTION_PERCENTAGE, \
    RENDER_TILE_SIZE, COLORS_SCALED, COLORS, FRAME_RATE, CAMERA_LOCATION, CAMERA_ANGLE, LAMP_TYPE
import bpy
import bobject
from copy import copy, deepcopy


def initialize_blender(total_duration=DEFAULT_SCENE_DURATION, clear_blender=True, vertical=False):
    # clear objects and materials
    # Reading the homefile would likely by faster, but it
    # sets the context to None, which breaks a bunch of
    # other stuff down the line. I don't know how to make the context not None.
    # bpy.ops.wm.read_homefile()
    if clear_blender:
        clear_blender_data()

    scn = bpy.context.scene
    scn.render.engine = 'CYCLES'
    scn.cycles.device = 'GPU'
    scn.cycles.samples = SAMPLE_COUNT
    scn.cycles.preview_samples = SAMPLE_COUNT
    scn.cycles.light_sampling_threshold = LIGHT_SAMPLING_THRESHOLD
    scn.cycles.transparent_max_bounces = 40
    scn.render.resolution_percentage = RESOLUTION_PERCENTAGE
    scn.render.use_compositing = False
    scn.render.use_sequencer = False
    scn.render.image_settings.file_format = 'PNG'
    scn.render.tile_x = RENDER_TILE_SIZE
    scn.render.tile_y = RENDER_TILE_SIZE
    scn.render.resolution_x = 1920
    scn.render.resolution_y = 1080
    if vertical:
        scn.render.resolution_x = 1080
        scn.render.resolution_y = 1920
    # Apparentlly 16-bit color depth pngs don't convert well to mp4 in Blender.
    # It gets all dark. 8-bit it is.
    # BUT WAIT. I can put stacks of pngs straight into premiere.
    scn.render.image_settings.color_depth = '16'
    scn.render.image_settings.color_mode = 'RGBA'
    scn.cycles.film_transparent = True

    # Set to 60 fps
    bpy.ops.script.execute_preset(
        filepath="C:\\Program Files\\Blender Foundation\\Blender\\2.79\\scripts\\presets\\framerate\\60.py",
        menu_idname="RENDER_MT_framerate_presets"
    )

    # Idfk how to do manipulate the context
    '''for area in bpy.context.screen.areas:
        if area.type == 'TIMELINE':
            bpy.context.area = area
            bpy.context.space_data.show_seconds = True'''

    # The line below makes it so Blender doesn't apply gamma correction. For some
    # reason, Blender handles colors differently from how every other program
    # does, and it's terrible. Why.
    # But this fixes it. Also, the RGB values you see in Blender
    # will be wrong, because the gamma correction is still applied when the color
    # is defined, but setting view_transform to 'Raw' undoes the correction in
    # render.
    scn.view_settings.view_transform = 'Raw'

    scn.gravity = (0, 0, -9.81)

    bpy.ops.world.new()
    world = bpy.data.worlds[-1]
    scn.world = world
    nodes = world.node_tree.nodes
    nodes.new(type='ShaderNodeMixRGB')
    nodes.new(type='ShaderNodeLightPath')
    nodes.new(type='ShaderNodeRGB')
    world.node_tree.links.new(nodes[2].outputs[0], nodes[1].inputs[0])
    world.node_tree.links.new(nodes[3].outputs[0], nodes[2].inputs[0])
    world.node_tree.links.new(nodes[4].outputs[0], nodes[2].inputs[2])
    nodes[4].outputs[0].default_value = COLORS_SCALED[0]

    define_materials()

    # set up timeline
    bpy.data.scenes["Scene"].frame_start = 0
    bpy.data.scenes["Scene"].frame_end = total_duration * FRAME_RATE - 1
    bpy.context.scene.frame_set(0)

    # create camera and light
    bpy.ops.object.camera_add(location=CAMERA_LOCATION, rotation=CAMERA_ANGLE)
    cam = bpy.data.cameras[0]
    # cam.type = 'ORTHO'
    cam.type = 'PERSP'
    cam.ortho_scale = 30

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 100))
    lamp_parent = bpy.context.object
    lamp_parent.name = 'Lamps'

    lamp_height = 35
    bpy.ops.object.lamp_add(type=LAMP_TYPE, location=(0, 0, lamp_height))
    lamp = bpy.context.object
    lamp.parent = lamp_parent
    lamp.matrix_parent_inverse = lamp.parent.matrix_world.inverted()
    lamp.data.node_tree.nodes[1].inputs[1].default_value = 1.57
    # lamp.data.shadow_soft_size = 3

    # Sets view to look through camera.
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            override = bpy.context.copy()
            override['area'] = area
            bpy.ops.view3d.viewnumpad(override, type='CAMERA')
            break


def clear_blender_data():
    print('Clearing Blender data')
    for bpy_data_iter in (
            bpy.data.objects,
            bpy.data.meshes,
            bpy.data.lamps,
            bpy.data.cameras,
            bpy.data.curves,
            bpy.data.materials,
            bpy.data.particles,
            bpy.data.worlds
    ):

        for id_data in bpy_data_iter:
            bpy_data_iter.remove(id_data)


def define_materials():
    clear = bpy.data.materials.new(name="clear")
    clear.use_nodes = True
    nodes = clear.node_tree.nodes
    nodes.remove(nodes[1])  # This is the diffuse shader by default
    nodes.new(type='ShaderNodeBsdfRefraction')
    nodes[1].inputs[0].default_value = (0.8, 1, 1, 1)
    # Hook up the refraction shader to the output (nodes[0])
    clear.node_tree.links.new(nodes[1].outputs[0], nodes[0].inputs[0])

    for i, col in enumerate(COLORS):
        name = 'color' + str(i + 1)
        make_basic_material(rgb=deepcopy(col), name=name)
        name = 'creature_color' + str(i + 1)
        make_creature_material(rgb=deepcopy(col), name=name)
        name = 'trans_color' + str(i + 1)
        make_translucent_material(rgb=deepcopy(col), name=name)


def make_basic_material(rgb=None, name=None):
    if rgb is None or name is None:
        raise Warning('Need rgb and name to make basic material')
    for i in range(3):
        # Range exactly 3 so a fourth component (alpha) isn't affected
        rgb[i] /= 255

    color = bpy.data.materials.new(name=name)
    color.use_nodes = True
    nodes = color.node_tree.nodes
    # nodes[1].inputs[1].default_value = 1 #Roughness. 1 means not shiny.
    nodes[1].inputs[0].default_value = rgb

    rgb = rgb[:3]  # Cuts to 3 components so it works for diffuse_color
    # which doesn't take alpha
    color.diffuse_color = rgb


def make_creature_material(rgb=None, name=None):
    if rgb is None or name is None:
        raise Warning('Need rgb and name to make creature material')
    for i in range(3):
        # Range exactly 3 so a fourth component (alpha) isn't affected
        rgb[i] /= 255

    color = bpy.data.materials.new(name=name)
    color.use_nodes = True
    nodes = color.node_tree.nodes
    # nodes[1].inputs[1].default_value = 1 #Roughness. 1 means not shiny.
    nodes.new(type='ShaderNodeBsdfPrincipled')
    nodes[2].inputs[0].default_value = rgb
    color.node_tree.links.new(nodes[2].outputs[0], nodes[0].inputs[0])

    rgb = rgb[:3]  # Cuts to 3 components so it works for diffuse_color
    # which doesn't take alpha
    color.diffuse_color = rgb


def make_translucent_material(rgb=None, name=None):
    if rgb is None or name is None:
        raise Warning('Need rgb and name to make translucent material')
    for i in range(3):
        # Range exactly 3 so a fourth component (alpha) isn't affected
        rgb[i] /= 255

    strength = 4  # Arbitrary, could make this a constant
    # strength = 0.1

    color = bpy.data.materials.new(name=name)
    color.use_nodes = True
    nodes = color.node_tree.nodes
    color.node_tree.links.remove(nodes[0].inputs[0].links[0])
    nodes.new(type='ShaderNodeAddShader')  # index 2
    color.node_tree.links.new(nodes[2].outputs[0], nodes[0].inputs[1])
    nodes.new(type='ShaderNodeAddShader')  # index 3
    color.node_tree.links.new(nodes[3].outputs[0], nodes[2].inputs[1])
    nodes.new(type='ShaderNodeEmission')  # index 4
    nodes[4].inputs[0].default_value = rgb
    nodes[4].inputs[1].default_value = strength
    color.node_tree.links.new(nodes[4].outputs[0], nodes[2].inputs[0])
    nodes.new(type='ShaderNodeVolumeScatter')  # index 5
    nodes[5].inputs[0].default_value = rgb
    nodes[5].inputs[1].default_value = strength
    color.node_tree.links.new(nodes[5].outputs[0], nodes[3].inputs[0])
    nodes.new(type='ShaderNodeVolumeAbsorption')  # index 6
    nodes[6].inputs[0].default_value = rgb
    nodes[6].inputs[1].default_value = strength
    color.node_tree.links.new(nodes[6].outputs[0], nodes[3].inputs[1])

    rgb = rgb[:3]  # Cuts to 3 components so it works for diffuse_color
    # which doesn't take alpha
    color.diffuse_color = rgb


def apply_material(obj, mat, recursive=False, type_req=None, intensity=None):
    if obj.type not in ['EMPTY', 'ARMATURE']:
        if type_req is None or obj.type == type_req:
            if isinstance(mat, str):
                obj.active_material = bpy.data.materials[mat]
            else:  # Assumes mat is a material.
                obj.active_material = mat

    if recursive:
        for child in obj.children:
            apply_material(child, mat, recursive=recursive, type_req=type_req)

    if intensity is not None and 'trans' in mat:
        nodes = obj.active_material.node_tree.nodes

        scat = nodes['Volume Scatter']
        absorb = nodes['Volume Absorption']
        emit = nodes['Emission']

        for node in [scat, absorb, emit]:
            node.inputs[1].default_value = intensity


def cam_and_swivel(
        cam_location=[25, 0, 0],
        cam_rotation_euler=[0, 0, 0],
        cam_name="Camera Bobject",
        swivel_location=[0, 0, 0],
        swivel_rotation_euler=[0, 0, 0],
        swivel_name='Cam swivel',
        control_sun=False
):
    cam_bobj = bobject.Bobject(
        location=cam_location,
        rotation_euler=cam_rotation_euler,
        name=cam_name
    )
    cam_swivel = bobject.Bobject(
        cam_bobj,
        location=swivel_location,
        rotation_euler=swivel_rotation_euler,
        name=swivel_name,
    )

    cam_obj = bpy.data.objects['Camera']
    cam_obj.data.clip_end = 100
    cam_obj.location = [0, 0, 0]
    cam_obj.parent = cam_bobj.ref_obj

    if control_sun == True:
        sun_obj = bpy.data.objects['Sun']
        sun_obj.location = [0, 0, 0]
        sun_obj.parent = cam_bobj.ref_obj

    return cam_bobj, cam_swivel


def link_descendants(obj, unlink=False, top_level=True):
    # If children exist, link those too
    # Will break if imported children were linked in add_to_blender
    # (if their object name in blender is the same as the filename)

    if unlink and top_level:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select = True

    obj_names = [x.name for x in bpy.data.objects]
    for child in obj.children:
        if not unlink:
            if child.name not in bpy.context.scene.objects:
                bpy.context.scene.objects.link(child)
        else:
            child.select = True
        link_descendants(child, unlink=unlink, top_level=False)
    if unlink:
        bpy.ops.object.delete()


def hide_self_and_descendants(obj, hide=True, keyframes=False, frame=None):
    # If hide == True, this hides everything.
    # If hide == False, this un-hides everything.

    if keyframes == True:
        if frame == None:
            raise Exception('in hide_self_and_descendants(), frame must be '
                            'specified if keyframes == True')
        obj.hide = hide
        obj.hide_render = hide
        obj.keyframe_insert(data_path='hide', frame=frame)
        obj.keyframe_insert(data_path='hide_render', frame=frame)
    else:
        obj.hide = hide
        obj.hide_render = hide
    for child in obj.children:
        hide_self_and_descendants(child, hide=hide, keyframes=keyframes, frame=frame)
