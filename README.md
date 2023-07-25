# GENEA Local renderer

A minimal code needed to run GENEA visualiser in local
- This one is based on the 2020 GENEA mesh, available from : https://github.com/jonepatr/genea_visualizer
- A newer version for 2022 and 2023 GENEA mesh are available on : https://github.com/TeoNikolov/genea_visualizer

If you need to use the 2023 3D mesh, should just need to replace the gesturer_mesh.fbx file (normally ?)

## Installation

- Install Blender (tested on Blender 2.83, 2.91 and 3.3)
- Install Python (>= 3.8, tested on 3.11)
- Install requirements.txt (pip install -r requirements.txt)
- Launch main.py script

## Tweaking

The repo is only 2 script, one to launch a render on multiple files/folders, the other is the actual blender script with several options :

### - main.py
All path should be absolute as the blender process will be separate, relative folders can break it :
- *blender_path* : The path to your blender executable
- *input_path* : The path to the base folder for input bvh
- *output_path* : The path to the base folder for output video
- *models* : This list depict all *input_path* subfolders to loop through

The script will just loop through all .bvh files found in each model subfolder.

### - blender_render.py
Those settings affect performance and quality of the final render :
- *bpy.context.scene.render.resolution_x* : Width of the output video
- *bpy.context.scene.render.resolution_y* : Height of the output video
- *bpy.context.scene.render.fps* : Framerate of the output video (.bvh data are scaled on the framerate)
- 3 rendering engines are available (end of the script), by default 'Workbench', the fastest one, is used, if you want to go fancy, I put Cycles & EEVEE code (with GPU/CUDA support)

If you need help, feel free to contact me !