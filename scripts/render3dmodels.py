#!/usr/bin/env python3
#====================================
# @file   : render3dmodels
# @brief  : Python script for blender which places all vessels in a scene to render the HUD images
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
import re
import bpy
import os
import mathutils
import shutil

def resize_scene_to_unit_box():
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
    scale_factor *= 11.0
    
    for obj in objects:
        # Move to origin relative to the scene center
        obj.location -= center
        # Scale uniformly
        obj.scale *= scale_factor
        # Apply current location offset scaled down
        obj.location *= scale_factor

def render_obj(file_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath="units/vessels/hud_render_template.blend")

    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Import the OBJ
    bpy.ops.wm.obj_import(
        filepath=os.path.abspath(file_path)
    )

    # Configure Transparency
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'

    # rendering quality
    bpy.context.scene.eevee.use_raytracing = True
    bpy.context.scene.eevee.ray_tracing_method = 'SCREEN'
    #bpy.context.scene.render.engine = 'CYCLES'
    #bpy.context.scene.cycles.samples = 256

    # Fix normal map strength which otherwise would be 0
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and obj.data.materials:
            for mat in obj.data.materials:
                if mat and mat.use_nodes and mat.node_tree:
                    # Look for the 'Normal Map' node
                    nodes = mat.node_tree.nodes
                    for node in nodes:
                        if node.type == 'NORMAL_MAP':
                            node.inputs['Strength'].default_value = 1.0
                            
                            # Follow the link from the 'Color' input
                            if node.inputs['Color'].is_linked:
                                img_node = node.inputs['Color'].links[0].from_node
                                if img_node.type == 'TEX_IMAGE' and img_node.image:
                                    img_node.image.colorspace_settings.name = 'Non-Color'
                                    print(f"Set Normal map texture '{img_node.image.name}' to Non-Color")

                    principled = next((n for n in nodes if n.type == 'BSDF_PRINCIPLED'), None)
                    
                    if principled:
                        ior_input = principled.inputs.get('Specular IOR Level')

                        # Trace back the connection if it exists
                        if ior_input and ior_input.is_linked:
                            # Get the node connected to the IOR Level input
                            link = ior_input.links[0]
                            image_node = link.from_node
                            
                            # Verify it is an image texture and set to Non-Color
                            if image_node.type == 'TEX_IMAGE' and image_node.image:
                                image_node.image.colorspace_settings.name = 'Non-Color'
                                image_node.image.update()
                                print(f"Set {image_node.name} connected to IOR Level to Non-Color")

    # Set Output
    bpy.context.scene.render.filepath = output_path
    
    # fit_camera_to_object(bpy.context.selected_objects[0])
    resize_scene_to_unit_box()

    # retain the blender file for debugging or refinement purposes
    blend_save_path = output_path.replace(".png", ".blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_save_path)
                                
    # Render
    bpy.ops.render.render(write_still=True)


def rewrite_mtl_file(src, target):
    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace 'map_Normal' with 'map_Bump'
    new_content = re.sub('map_Ka.*','', 
        re.sub('map_Kd .*\\.ani', 'd 0.0', 
        content.replace('map_Normal', '#')
        .replace('map_Bump', 'map_Bump -bm 1.000000')
        .replace('.texture', '.png')
        .replace('AeraHull.png', os.path.relpath('./textures/AeraHull.png', os.path.dirname(target)))
        .replace('black.png', os.path.relpath('./textures/black.png', os.path.dirname(target)))
        .replace('combine2.bmp', os.path.relpath('./textures/combine2.png', os.path.dirname(target)))
        .replace('combine4.bmp', os.path.relpath('./textures/combine4.png', os.path.dirname(target)))
        .replace('combine.bmp', os.path.relpath('./textures/combine.bmp', os.path.dirname(target)))
        .replace('combine.jpg', os.path.relpath('./textures/combine.jpg', os.path.dirname(target)))
        .replace('glass.png', os.path.relpath('./textures/glass.png', os.path.dirname(target)))
        .replace('shield.bmp', os.path.relpath('./textures/shield.bmp', os.path.dirname(target)))
        .replace('shield_generic.png', os.path.relpath('./textures/shield_generic.png', os.path.dirname(target)))
        .replace('white.bmp', os.path.relpath('./textures/white.bmp', os.path.dirname(target)))
        ))
    
    # proper texture references for hyena
    # map_Kd hyena.png
    # map_Ks hyena_spec.png
    # map_Ka hyena_dmg.png
    # map_Ke hyenaGLO.png
    # map_Normal HyenaNormal.png

    with open(target, 'w', encoding='utf-8') as f:
        f.write(new_content)

def my_custom_copy(src, dst):
    # Check if it's an .mtl file
    if src.lower().endswith('.mtl'):
        rewrite_mtl_file(src, dst)
    else:
        # For all other files (obj, png, etc.), use the standard copy
        shutil.copy2(src, dst)

if(__name__ == "__main__"):
    # source_dir = "./tmp/"
    vessels_root = './units/vessels'
    target_dir = "./build/"

    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # copy all generated files from tmp to build, overwriting existing files
    # shutil.copytree(
    #     source_dir, 
    #     target_dir, 
    #     dirs_exist_ok=True,
    #     ignore=shutil.ignore_patterns('*.tmp', '.git'),
    #     copy_function=my_custom_copy
    # )

    # copy all OBJ, MTL, PNG, and JPG files from vessels_root to target_dir, overwriting generated files with sources
    for current_dir, _, files in os.walk(vessels_root):
        for file in files:
            file_path = os.path.join(current_dir, file)
            name, ext = os.path.splitext(file)
            ext = ext.lower()
            target_file = os.path.join(target_dir, os.path.relpath(file_path, "."))
            os.makedirs(os.path.dirname(target_file), exist_ok=True)

            # 1. Handle OBJ files
            if ext == '.obj':
                shutil.copy2(file_path, target_file)
                print(f"Copied OBJ: {file}")

            # 2. Handle MTL files (with text replacement)
            elif ext == '.mtl':
                rewrite_mtl_file(file_path, target_file)
                print(f"Processed MTL: {file}")

            # 3. Handle PNG and JPG/JPEG files
            elif ext in ['.png', '.jpg', '.jpeg'] and not name.lower().endswith(('-hud')) and not current_dir.lower().endswith('sources'):
                # Check if parent folder matches an OBJ filename (without extension)
                parent_folder_name = os.path.basename(current_dir)
                
                # Optional: Add check here if parent_folder_name corresponds to an obj in source_root
                # Copy to target directory
                shutil.copy2(file_path, target_file)
                print(f"Copied Image: {file_path} to {target_file}")
            
    # now render all OBJ files in the target_dir to generate HUD images
    for current_dir, _, files in os.walk(target_dir):
        for file in files:
            exclude_keywords = ['marker','shield', '-mount', 'turret', "acrotatus", "aidi", "anaxander", "catfish", "ct1000", "ct3000", "ellison", "lemma", "nietzsche", "patterson"]
            if file.endswith((".obj")) and not any(keyword in file.lower() for keyword in exclude_keywords):
                obj_path = os.path.join(current_dir, file)
                output_path = os.path.join(target_dir,"hud", f"{os.path.splitext(file)[0]}-hud.png")
                render_obj(obj_path, output_path)


# vega-meshtool --input tri.bfxm --output tri.obj --convert BFXM Wavefront create