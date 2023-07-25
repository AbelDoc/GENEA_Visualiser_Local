# Copyright 2020 by Patrik Jonell.
# All rights reserved.
# This file is part of the GENEA visualizer,
# and is released under the GPLv3 License. Please see the LICENSE
# file that should have been included as part of this package.

# Modified by Louis ABEL, 2023

import glob
import os
import subprocess
import sys
from pathlib import Path

from tqdm import tqdm


def render(input, output, blender_path):
    subprocess.check_call(
        [
            blender_path,
            "-b",
            "-noaudio",
            "--python",
            "blender_render.py",
            "--",
            input,
            output,
        ],
        shell=True,
        # If you want to silence blender process, use DEVNULL
        stdout=sys.stdout,
        # stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main():
    # All path should be absolute as Blender tends to be used in a separate process, relative path won't work
    blender_path = "C:/Program Files/Blender Foundation/Blender 3.3/blender.exe"
    input_path = ""
    output_path = ""

    models = [
    ]

    for model in tqdm(models, desc="Animating models..."):
        input_dir = os.path.join(input_path, model)
        output_dir = os.path.join(output_path, model)

        os.makedirs(output_dir, exist_ok=True)

        for file in tqdm(glob.glob(os.path.join(input_dir, "*.bvh")), desc="Animating files"):
            render(file, os.path.join(output_dir, "{}_video.mp4".format(Path(file).stem)), blender_path)


if __name__ == "__main__":
    main()
