#!/usr/bin/env python3
#====================================
# @file   : render3dmodels
# @brief  : Python script for blender which places all BFMX files in a directory in a scene and renders them
# @author : Danny Gehl (SGD1953)
#====================================
# Copyright (C) 2026 Evert Vorster, Stephen G. Tuggy, Roy Falk,
# Benjamen R. Meyer, SGD1953, and other vsUTCS contributors.
#
# This file is part of Vega Strike: Upon the Coldest Sea ("vsUTCS").
#
# vsUTCS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# vsUTCS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with vsUTCS.  If not, see <https://www.gnu.org/licenses/>.
import fnmatch
import math
from pathlib import Path

import bpy
import argparse
import os
import sys
import mathutils

def setup_argparse():
    # Blender passes arguments after '--'
    args_list = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    
    parser = argparse.ArgumentParser(description="Batch render Blender scenes.")
    parser.add_argument("--source", default="units/vessels", help="Source directory")
    parser.add_argument("--target", default="build", help="Output directory")
    parser.add_argument("--template", default="units/vessels/hud_render_template.blend", help="Blender template path")
    parser.add_argument("--ignore", nargs='*', default=["blink*", "greenlight*", "shield*", "*Shield*"], 
                        help="List of patterns to ignore (e.g., blink* greenlight* shield*)")
    return parser.parse_args(args_list)

def resize_scene_to_unit_box(scale_modifier=1.0):
    # 1. Collect all mesh objects
    objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    if not objects:
        return

    # 2. Calculate the global bounding box
    # Initialize with extreme values
    min_x = min_y = min_z = float('inf')
    max_x = max_y = max_z = float('-inf')

    for obj in objects:
        # Get world-space corners of the object's bounding box
        bbox = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
        for corner in bbox:
            min_x, max_x = min(min_x, corner.x), max(max_x, corner.x)
            min_y, max_y = min(min_y, corner.y), max(max_y, corner.y)
            min_z, max_z = min(min_z, corner.z), max(max_z, corner.z)

    # 3. Calculate current dimensions and center
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    
    center = mathutils.Vector(((min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2))
    
    # Max dimension to ensure it fits within 1x1x1
    max_dim = max(width, depth, height)
    if max_dim == 0: return # Prevent division by zero

    # 4. Apply transformation to all objects
    scale_factor = 1.0 / max_dim
    # correct the scale factor by 11, why? ¯\_(ツ)_/¯
    scale_factor *= 11.0 * scale_modifier
    
    for obj in objects:
        # Move to origin relative to the scene center
        obj.location -= center
        # Scale uniformly
        obj.scale *= scale_factor
        # Apply current location offset scaled down
        obj.location *= scale_factor

def should_ignore(filename, patterns):
    for pattern in patterns:
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False

def process_files():
    args = setup_argparse()
    
    for root, dirs, files in os.walk(args.source):
        # Find all *_0.xmesh files in the current directory
        xmesh_files = [
            f for f in files 
            if f.endswith("_0.xmesh") and not should_ignore(f, args.ignore)
        ]
        path = Path(root)
        
        if not xmesh_files:
            continue
            
        # Create corresponding target directory
        relative_path = os.path.relpath(root, ".")
        output_dir = os.path.join(args.target, relative_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # Open template
        bpy.ops.wm.open_mainfile(filepath=args.template)
        
        # Import your files (Assuming a custom importer or generic logic)
        # Note: You may need a specific operator here based on how you import .xmesh
        for xmesh in xmesh_files:
            file_path = os.path.join(root, xmesh)
            bpy.ops.import_scene.xmesh(filepath=file_path)
            print(f"Importing: {file_path}")

        # Now rotate into the XY plane
        for obj in [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']:
            # Rotation is in radians. 90 degrees = pi / 2
            obj.rotation_euler[0] += math.radians(90)

        scale_factors = {
            "Charillus": .7,
            "Derivative" : .7, 
            "Gaozong" : .7,
            "GTIO": .7, 
            "Hammer": .7, 
            "Plowshare": .7, 
            "Ruizong": .7, 
            "Schroedinger": .7, 
            "Shizu": .7, 
            "Zhuangzong": .8
        }
        scale_factor = scale_factors.get(path.name, 1.0)

        print(f"Vessel name: {path.name} - scaling with {scale_factor}")
        resize_scene_to_unit_box(scale_factor)

            
        # Setup output path
        render_path = os.path.join(output_dir, f"{path.name}-hud.png")
        bpy.context.scene.render.filepath = render_path
        
        # Render
        bpy.ops.render.render(write_still=True)
        print(f"Rendered to: {render_path}")

if __name__ == "__main__":
    process_files()