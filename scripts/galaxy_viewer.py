# /// script
# dependencies = [
#   "PyOpenGL",
#   "pygame",
#   "numpy",
# ]
# ///
#====================================
# @file   : build
# @brief  : Python script to view galaxy maps in a side-by-side comparison mode using OpenGL and Pygame.
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

import sys
import os
import struct
import pygame
from pygame.locals import *
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

# CONFIGURATION
WINDOW_SIZE = (1600, 900)  # Wider canvas to cleanly fit two viewports side-by-side
ROTATION_SPEED = 2.0 

# Official OpenGL specification face orientation order (+X, -X, +Y, -Y, +Z, -Z)
FACE_ORDER = ["right", "left", "top", "bottom", "front", "back"]

GL_CUBE_MAP_TARGETS = {
    "right":  GL_TEXTURE_CUBE_MAP_POSITIVE_X,
    "left":   GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
    "top":    GL_TEXTURE_CUBE_MAP_POSITIVE_Y,
    "bottom": GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
    "front":  GL_TEXTURE_CUBE_MAP_POSITIVE_Z,
    "back":   GL_TEXTURE_CUBE_MAP_NEGATIVE_Z
}

yaw = 0.0
pitch = 0.0

def decompress_dxt1_to_rgba(data, width, height):
    num_blocks_x = width // 4
    num_blocks_y = height // 4
    rgba_output = np.zeros((height, width, 4), dtype=np.uint8)
    
    block_dtype = np.dtype([('color0', '<u2'), ('color1', '<u2'), ('bits', '<u4')])
    blocks = np.frombuffer(data[:num_blocks_x * num_blocks_y * 8], dtype=block_dtype)
    
    c0 = blocks['color0'].astype(np.uint32)
    c1 = blocks['color1'].astype(np.uint32)
    
    r0, g0, b0 = ((c0 >> 11) & 0x1F) << 3, ((c0 >> 5) & 0x3F) << 2, (c0 & 0x1F) << 3
    r1, g1, b1 = ((c1 >> 11) & 0x1F) << 3, ((c1 >> 5) & 0x3F) << 2, (c1 & 0x1F) << 3
    
    r2, g2, b2 = (2 * r0 + r1) // 3, (2 * g0 + g1) // 3, (2 * b0 + b1) // 3
    r3, g3, b3 = (r0 + 2 * r1) // 3, (g0 + 2 * g1) // 3, (b0 + 2 * b1) // 3
    
    colors = np.zeros((len(blocks), 4, 4), dtype=np.uint8)
    colors[:, 0, 0:3] = np.stack([r0, g0, b0], axis=-1)
    colors[:, 1, 0:3] = np.stack([r1, g1, b1], axis=-1)
    colors[:, 2, 0:3] = np.stack([r2, g2, b2], axis=-1)
    colors[:, 3, 0:3] = np.stack([r3, g3, b3], axis=-1)
    colors[:, :, 3] = 255
    
    bits = blocks['bits']
    for y_offset in range(4):
        for x_offset in range(4):
            code = (bits >> (2 * (y_offset * 4 + x_offset))) & 0x03
            block_idx = np.arange(len(blocks))
            rgba_output[
                (block_idx // num_blocks_x) * 4 + y_offset,
                (block_idx % num_blocks_x) * 4 + x_offset
            ] = colors[block_idx, code]
            
    return rgba_output.tobytes()

def load_dds_cubemap(path):
    if not os.path.exists(path):
        print(f"Error: File '{path}' not found.")
        sys.exit(1)

    with open(path, "rb") as f:
        data = f.read()

    if data[0:4] != b"DDS ":
        print(f"Error: '{path}' is not a valid DDS container.")
        sys.exit(1)

    height, width = struct.unpack("<II", data[12:20])
    fourcc = data[84:88]
    header_offset = 148 if fourcc == b"DX10" else 128
    pixel_data = data[header_offset:]
    
    face_data_size = len(pixel_data) // 6
    base_dxt1_size = (width * height) // 2

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_CUBE_MAP, tex_id)

    print(f"Unpacking {os.path.basename(path)} ({width}x{height})...")

    for idx, face_name in enumerate(FACE_ORDER):
        gl_target = GL_CUBE_MAP_TARGETS[face_name]
        start_byte = idx * face_data_size
        face_bytes = pixel_data[start_byte : start_byte + base_dxt1_size]
        
        rgba_bytes = decompress_dxt1_to_rgba(face_bytes, width, height)
        glTexImage2D(gl_target, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, rgba_bytes)

    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
    
    return tex_id

def draw_skybox():
    glBegin(GL_QUADS)
    # Front Face
    glTexCoord3f(-1.0, -1.0,  1.0); glVertex3f(-1.0, -1.0,  1.0)
    glTexCoord3f( 1.0, -1.0,  1.0); glVertex3f( 1.0, -1.0,  1.0)
    glTexCoord3f( 1.0,  1.0,  1.0); glVertex3f( 1.0,  1.0,  1.0)
    glTexCoord3f(-1.0,  1.0,  1.0); glVertex3f(-1.0,  1.0,  1.0)
    # Back Face
    glTexCoord3f( 1.0, -1.0, -1.0); glVertex3f( 1.0, -1.0, -1.0)
    glTexCoord3f(-1.0, -1.0, -1.0); glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord3f(-1.0,  1.0, -1.0); glVertex3f(-1.0,  1.0, -1.0)
    glTexCoord3f( 1.0,  1.0, -1.0); glVertex3f( 1.0,  1.0, -1.0)
    # Top Face
    glTexCoord3f(-1.0,  1.0,  1.0); glVertex3f(-1.0,  1.0,  1.0)
    glTexCoord3f( 1.0,  1.0,  1.0); glVertex3f( 1.0,  1.0,  1.0)
    glTexCoord3f( 1.0,  1.0, -1.0); glVertex3f( 1.0,  1.0, -1.0)
    glTexCoord3f(-1.0,  1.0, -1.0); glVertex3f(-1.0,  1.0, -1.0)
    # Bottom Face
    glTexCoord3f(-1.0, -1.0, -1.0); glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord3f( 1.0, -1.0, -1.0); glVertex3f( 1.0, -1.0, -1.0)
    glTexCoord3f( 1.0, -1.0,  1.0); glVertex3f( 1.0, -1.0,  1.0)
    glTexCoord3f(-1.0, -1.0,  1.0); glVertex3f(-1.0, -1.0,  1.0)
    # Right Face
    glTexCoord3f( 1.0, -1.0,  1.0); glVertex3f( 1.0, -1.0,  1.0)
    glTexCoord3f( 1.0, -1.0, -1.0); glVertex3f( 1.0, -1.0, -1.0)
    glTexCoord3f( 1.0,  1.0, -1.0); glVertex3f( 1.0,  1.0, -1.0)
    glTexCoord3f( 1.0,  1.0,  1.0); glVertex3f( 1.0,  1.0,  1.0)
    # Left Face
    glTexCoord3f(-1.0, -1.0, -1.0); glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord3f(-1.0, -1.0,  1.0); glVertex3f(-1.0, -1.0,  1.0)
    glTexCoord3f(-1.0,  1.0,  1.0); glVertex3f(-1.0,  1.0,  1.0)
    glTexCoord3f(-1.0,  1.0, -1.0); glVertex3f(-1.0,  1.0, -1.0)
    glEnd()

def render_scene(tex_id, view_w, view_h, pitch, yaw):
    """ Sets up context projection matrix properties for a single scene viewport """
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(75, (view_w / view_h), 0.1, 50.0)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(pitch, 1.0, 0.0, 0.0)
    glRotatef(yaw, 0.0, 1.0, 0.0)
    
    glBindTexture(GL_TEXTURE_CUBE_MAP, tex_id)
    draw_skybox()

def main():
    # Resolve argument parameter layout paths
    args = sys.argv[1:]
    img1, img2 = None, None
    is_dual_mode = False

    if len(args) == 0:
        print("You can pass one path parameter to view a single galaxy or two parameters to view 2 galaxies side-by-side.")
        print("python galaxy_viewer.py <path_to_first_galaxy.cube> [<path_to_second_galaxy.cube>]")
        exit(1)
    elif len(args) == 1:
        img1 = args[0]
    else:
        img1 = args[0]
        img2 = args[1]
        is_dual_mode = True

    pygame.init()
    # If single mode, scale down width to standard view dimensions
    win_w, win_h = WINDOW_SIZE if is_dual_mode else (800, 600)
    pygame.display.set_mode((win_w, win_h), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("VegaStrike Galaxy Comparison Engine")

    glEnable(GL_TEXTURE_CUBE_MAP)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Compile images sequentially into independent OpenGL descriptors
    tex1 = load_dds_cubemap(img1)
    tex2 = load_dds_cubemap(img2) if is_dual_mode else None

    yaw, pitch = 0.0, 0.0
    clock = pygame.time.Clock()
    running = True

    print("\n--- Map View Engine Ready ---")
    print("ARROW KEYS : Pan view inside loaded assets simultaneously")
    print("ESCAPE     : Quit application\n")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:  yaw -= ROTATION_SPEED
        if keys[K_RIGHT]: yaw += ROTATION_SPEED
        if keys[K_UP]:    pitch = min(89.0, pitch + ROTATION_SPEED)
        if keys[K_DOWN]:  pitch = max(-89.0, pitch - ROTATION_SPEED)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if not is_dual_mode:
            # Single Full-Window Viewport Context
            glViewport(0, 0, win_w, win_h)
            render_scene(tex1, win_w, win_h, pitch, yaw)
        else:
            # Side-by-Side Dual Viewport Splitting
            half_width = win_w // 2
            
            # Left Viewport Panel
            glViewport(0, 0, half_width, win_h)
            render_scene(tex1, half_width, win_h, pitch, yaw)
            
            # Right Viewport Panel
            glViewport(half_width, 0, half_width, win_h)
            render_scene(tex2, half_width, win_h, pitch, yaw)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
