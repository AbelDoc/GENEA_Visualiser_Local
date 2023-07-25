# Copyright 2020 by Patrik Jonell.
# All rights reserved.
# This file is part of the GENEA visualizer,
# and is released under the GPLv3 License. Please see the LICENSE
# file that should have been included as part of this package.

# Modified by Louis ABEL, 2023

import os

import bpy
from bpy import context
import sys


def fix_obj(parent_obj, mat):
    for obj in parent_obj.children:
        fix_obj(obj, mat)
    parent_obj.rotation_euler.x = 0
    if parent_obj.name in ["pCube0", "pCube1", "pCube2"]:
        parent_obj.location.y = -13
    if parent_obj.name == "pCube3":
        parent_obj.location.y = -10
    if parent_obj.name == "pCube5":
        parent_obj.location.y = -9.5

    if "materials" in dir(parent_obj.data):
        if parent_obj.data.materials:
            parent_obj.data.materials[0] = mat
        else:
            parent_obj.data.materials.append(mat)


def render_bvh(input, output):

    bpy.data.objects.remove(bpy.data.objects["Cube"], do_unlink=True)

    bpy.ops.import_scene.fbx(
        filepath=os.path.join(os.path.dirname(__file__), "gesturer_mesh.fbx"),
        global_scale=1,
        automatic_bone_orientation=True,
        axis_up="Y",
    )

    bpy.context.scene.render.filepath = output
    bpy.context.scene.render.image_settings.file_format = "FFMPEG"
    bpy.context.scene.render.ffmpeg.format = "MPEG4"
    bpy.context.scene.render.ffmpeg.codec = "H264"

    # 1080p @ 60fps
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.fps = 60

    fbx_model = context.scene.objects["Armature"]

    camera = bpy.data.objects["Camera"]
    camera.location = (0, -1.54, 0.42)
    camera.rotation_euler = (1.57, 0.0, 0)

    lamp = bpy.data.objects["Light"]
    lamp.location = (0.0, -6, 0)

    if not fbx_model.animation_data:
        fbx_model.animation_data_create()
    fbx_model.animation_data.action = None

    mat = bpy.data.materials["Material"]
    fix_obj(fbx_model, mat)

    old_objs = set(context.scene.objects)
    bpy.ops.import_anim.bvh(filepath=input, global_scale=0.01, use_fps_scale=True)

    (bvh_obj,) = set(context.scene.objects) - old_objs

    for pb in fbx_model.pose.bones:
        ct = pb.constraints.new("COPY_ROTATION")
        ct.owner_space = "WORLD"
        ct.target_space = "WORLD"
        ct.name = pb.name
        ct.target = bvh_obj
        ct.subtarget = pb.name

    action = bvh_obj.animation_data.action
    total_frames = int(action.frame_range.y)

    for i in range(int(action.frame_range.x), total_frames):
        context.scene.frame_set(i)
        for pb in fbx_model.pose.bones:
            m = fbx_model.convert_space(pose_bone=pb, matrix=pb.matrix, to_space="LOCAL")

            if pb.rotation_mode == "QUATERNION":
                pb.rotation_quaternion = m.to_quaternion()
                pb.keyframe_insert("rotation_quaternion", frame=i)
            else:
                pb.rotation_euler = m.to_euler(pb.rotation_mode)
                pb.keyframe_insert("rotation_euler", frame=i)

            pb.keyframe_insert("location", frame=i)
    bpy.context.scene.frame_end = total_frames

    # -- Uncomment to use cycles (slowest)
    # for scene in bpy.data.scenes:
    #     scene.cycles.device = 'GPU'
    #     scene.render.engine = "CYCLES"
    #
    # bpy.context.scene.cycles.samples = 64
    # bpy.context.scene.cycles.tile_x = 256
    # bpy.context.scene.cycles.tile_y = 256
    # bpy.context.scene.cycles.max_bounces = 1

    # -- Uncomment to use basic workbench (fastest)
    bpy.context.scene.render.engine = "BLENDER_WORKBENCH"

    # -- Uncomment to use eevee (in between)
    # bpy.context.scene.render.engine = "BLENDER_EEVEE"
    # bpy.context.scene.eevee.taa_render_samples = 8
    # bpy.context.scene.eevee.use_gtao = True
    # bpy.context.scene.eevee.use_bloom = False
    # bpy.context.scene.eevee.use_ssr = False

    bpy.ops.render.render(animation=True, write_still=False)
    bpy.ops.wm.quit_blender()


if __name__ == "__main__":
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]

    render_bvh(argv[0], argv[1])
    sys.exit(0)
