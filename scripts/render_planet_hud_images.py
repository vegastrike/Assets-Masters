#====================================
# @file   : script/render_planet_hud_images-py
# @brief  : Python script to render planet hud images using the appropriate textures in this repository.
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
import math

import bpy
import json
import os
import argparse
import sys

def setup_render_settings(res_x, res_y):
    scene = bpy.context.scene
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y
    scene.render.film_transparent = True  # Ensures background is transparent
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU' # Or 'CPU' if you don't have a GPU

def add_atmosphere(planet_obj, color=(0.5, 0.7, 1.0), density=0.2):
    # 1. Create a slightly larger sphere for the atmosphere
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.03)
    atmo = bpy.context.active_object
    atmo.name = "Atmosphere"
    bpy.ops.object.shade_smooth()

    # 2. Create Volumetric Material
    mat = bpy.data.materials.new(name="AtmosphereMaterial")
    nodes = mat.node_tree.nodes
    nodes.clear() # Clear default nodes

    # Shader setup: Volume Scatter + Material Output
    vol_scatter = nodes.new('ShaderNodeVolumeScatter')
    vol_scatter.inputs['Color'].default_value = (*color, 1.0)
    vol_scatter.inputs['Density'].default_value = density
    
    # Layer Weight for Fresnel (makes it transparent in the middle, thick at edges)
    fresnel = nodes.new('ShaderNodeLayerWeight')
    fresnel.inputs['Blend'].default_value = 0.5
    
    mix = nodes.new('ShaderNodeMixShader')
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    
    output = nodes.new('ShaderNodeOutputMaterial')

    # Links
    mat.node_tree.links.new(fresnel.outputs['Facing'], mix.inputs['Fac'])
    mat.node_tree.links.new(transparent.outputs['BSDF'], mix.inputs[1])
    mat.node_tree.links.new(vol_scatter.outputs['Volume'], mix.inputs[2])
    mat.node_tree.links.new(mix.outputs['Shader'], output.inputs['Volume'])

    atmo.data.materials.append(mat)

def add_clouds(planet_obj, cloud_tex_path):
    # 1. Create a slightly larger sphere for the clouds (e.g., 1.01 scale)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.01)
    cloud_shell = bpy.context.active_object
    cloud_shell.name = "Clouds"
    cloud_shell.parent = planet_obj
    bpy.ops.object.shade_smooth()

    # 2. Setup Material
    mat = bpy.data.materials.new(name="CloudMaterial")
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")

    # Load Texture
    tex_node = nodes.new('ShaderNodeTexImage')
    tex_node.image = bpy.data.images.load(os.path.abspath(cloud_tex_path))
    
    # Connect color to Base Color and alpha to Alpha
    mat.node_tree.links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])
    mat.node_tree.links.new(tex_node.outputs['Alpha'], bsdf.inputs['Alpha'])
    
    # Set material blend mode to Alpha Hashed or Alpha Blend
    mat.blend_method = 'HASHED'
    
    cloud_shell.data.materials.append(mat)

def render_planet(planet_key, planet_data, output_dir):
    # Clear existing
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Create Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1)
    planet = bpy.context.active_object
    bpy.ops.object.shade_smooth()

    # Material Setup
    mat = bpy.data.materials.new(name=planet_key)
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")

    # Enhance Material realism
    bsdf.inputs['Subsurface Weight'].default_value = 0.1 # Soft light scattering
    material_type = planet_data.get('material_type', 'rock') # Default to rock
    clearcoat = 0.0
    subsurface = 0.0

    if material_type == 'water':
        clearcoat = 0.6
        subsurface = 0.1
    elif material_type == 'ice':
        clearcoat = 0.3
        subsurface = 0.2
        
    bsdf.inputs['Coat Weight'].default_value = clearcoat
    bsdf.inputs['Coat Roughness'].default_value = 0.05
    bsdf.inputs['Subsurface Weight'].default_value = subsurface

    atmo_cfg = planet_data.get('atmosphere', {})
    if atmo_cfg:
        # Default to Earth-like if keys missing
        col = atmo_cfg.get('color', (0.5, 0.7, 1.0))
        dens = atmo_cfg.get('density', 0.2)
        add_atmosphere(planet, color=col, density=dens)

    # Base Color
    base_tex = nodes.new('ShaderNodeTexImage')
    base_tex.image = bpy.data.images.load(os.path.abspath(planet_data['base_texture']))
    mat.node_tree.links.new(base_tex.outputs['Color'], bsdf.inputs['Base Color'])

    # This creates a "halo" effect on the dark side of the planet
    nodes = mat.node_tree.nodes
    fresnel = nodes.new('ShaderNodeLayerWeight')
    fresnel.inputs['Blend'].default_value = 0.8
    
    # Use a Color Ramp to control the thickness of the rim glow
    ramp = nodes.new('ShaderNodeValToRGB')
    mat.node_tree.links.new(fresnel.outputs['Facing'], ramp.inputs['Fac'])
    
    # Mix this into your Emission input
    add_mix = nodes.new('ShaderNodeMix')
    add_mix.data_type = 'RGBA'
    mat.node_tree.links.new(ramp.outputs['Color'], add_mix.inputs[6])
    mat.node_tree.links.new(add_mix.outputs[2], bsdf.inputs['Emission Color'])

    if planet_data.get('specular'):
        spec_tex = nodes.new('ShaderNodeTexImage')
        spec_tex.image = bpy.data.images.load(os.path.abspath(planet_data['specular']))
        spec_tex.image.colorspace_settings.name = 'Non-Color'
        mat.node_tree.links.new(spec_tex.outputs['Color'], bsdf.inputs['Specular IOR Level'])

    # Lights
    if planet_data.get('lights'):
        light_tex = nodes.new('ShaderNodeTexImage')
        light_tex.image = bpy.data.images.load(os.path.abspath(planet_data['lights']))
        mat.node_tree.links.new(light_tex.outputs['Color'], bsdf.inputs['Emission Color'])
        bsdf.inputs['Emission Strength'].default_value = 2.0

    # Normal Map
    if planet_data.get('normal'):
        norm_tex = nodes.new('ShaderNodeTexImage')
        norm_tex.image = bpy.data.images.load(os.path.abspath(planet_data['normal']))
        norm_tex.image.colorspace_settings.name = 'Non-Color'
        norm_map = nodes.new('ShaderNodeNormalMap')
        mat.node_tree.links.new(norm_tex.outputs['Color'], norm_map.inputs['Color'])
        mat.node_tree.links.new(norm_map.outputs['Normal'], bsdf.inputs['Normal'])

    if planet_data.get('clouds'):
        add_clouds(planet, planet_data['clouds'])

    planet.data.materials.append(mat)

    # Setup Camera/Sun
    cam = bpy.data.cameras.new("Camera")
    cam_obj = bpy.data.objects.new("Camera", cam)
    bpy.context.collection.objects.link(cam_obj)
    cam_obj.location = (0, -3, 0)
    cam_obj.rotation_euler = (1.57, 0, 0)
    bpy.context.scene.camera = cam_obj

    sun = bpy.data.lights.new("Sun", type='SUN')
    sun.angle = math.radians(1.0)
    sun_obj = bpy.data.objects.new("Sun", sun)
    bpy.context.collection.objects.link(sun_obj)
    sun_obj.location = (5, -2, 5) 
    
    # Point the sun specifically at the sphere origin
    constraint = sun_obj.constraints.new(type='TRACK_TO')
    constraint.target = planet
    constraint.track_axis = 'TRACK_NEGATIVE_Z'

    # Add a Rim Light for depth
    rim_light = bpy.data.lights.new("RimLight", type='POINT')
    rim_obj = bpy.data.objects.new("RimLight", rim_light)
    bpy.context.collection.objects.link(rim_obj)
    
    rim_obj.location = (-8, 8, 2) 
    rim_light.energy = 500
    rim_light.shadow_soft_size = 5.0 # This blurs the light edge, removing the "dot"
    rim_light.color = (0.7, 0.8, 1.0)

    # Render
    os.makedirs(output_dir, exist_ok=True)
    bpy.context.scene.render.filepath = os.path.join(output_dir, f"planet-{planet_key}-hud.png")
    bpy.ops.render.render(write_still=True)

def main():
    # Parsing arguments passed after '--'
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", default="sprites/planets.json", help="Path to JSON")
    parser.add_argument("--output", default="build/sprites/", help="Output directory")
    parser.add_argument("--res", type=int, default=512, help="Resolution (square)")
    args = parser.parse_args(argv)

    setup_render_settings(args.res, args.res)

    with open(args.json, 'r') as f:
        planets = json.load(f)["planets"]

    for key, data in planets.items():
        render_planet(key, data, args.output)

if __name__ == "__main__":
    main()