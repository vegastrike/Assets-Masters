#!/usr/bin/env python3
#====================================
# @file   : scripts/povray/dds_cubemap.py
# @brief  : Assemble a DXT1/3/5 DDS cubemap from six single-face DDS files.
#====================================
# Copyright (C) 2026 Evert Vorster, Stephen G. Tuggy, Roy Falk,
# Benjamen R. Meyer, and other vsUTCS contributors.
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
#
"""Assemble a DXT1/3/5 DDS cubemap from six single-face DDS files.

Vega Strike loads backgrounds as a compressed DDS cubemap named
`<name>_light.cube`. Its DDS reader (engine/src/gfx/vsimage.cpp ReadDDS)
accepts only DXT1/DXT3/DXT5, and expects the six faces in the standard
DDS cubemap order: +X, -X, +Y, -Y, +Z, -Z.

No tool on this system writes a compressed DDS cubemap: cmft writes a
cubemap but only uncompressed (rejected by the engine), and ImageMagick
writes DXT1/DXT5 but only as a flat 2D image. So compress each face with
ImageMagick first, then concatenate them here.

Usage:
    dds_cubemap.py out.cube posx.dds negx.dds posy.dds negy.dds posz.dds negz.dds
"""
import struct
import sys

DDS_HEADER_SIZE = 128
DDS_CAPS_COMPLEX = 0x8
DDS_CAPS_TEXTURE = 0x1000
DDS_CAPS_MIPMAP = 0x400000
DDS_CUBEMAP_ALLFACES = 0xFE00  # DDS_CUBEMAP | the six per-face flags


def read_face(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:4] != b"DDS ":
        raise SystemExit(f"{path}: not a DDS file")
    if len(data) < DDS_HEADER_SIZE:
        raise SystemExit(f"{path}: truncated DDS header")
    fourcc = data[84:88]
    if fourcc[:3] != b"DXT" or fourcc[3:4] not in (b"1", b"3", b"5"):
        raise SystemExit(f"{path}: face must be DXT1/3/5, got {fourcc!r}")
    return data


def build_header(face):
    """Copy the face header and mark it as a full six-face cubemap."""
    header = bytearray(face[:DDS_HEADER_SIZE])
    caps = DDS_CAPS_COMPLEX | DDS_CAPS_TEXTURE | DDS_CAPS_MIPMAP
    struct.pack_into("<I", header, 108, caps)
    struct.pack_into("<I", header, 112, DDS_CUBEMAP_ALLFACES)
    return bytes(header)


def main(argv):
    if len(argv) != 8:
        raise SystemExit(__doc__.strip().splitlines()[-1])
    out_path, face_paths = argv[1], argv[2:]
    faces = [read_face(p) for p in face_paths]

    sizes = {len(f) for f in faces}
    if len(sizes) != 1:
        raise SystemExit(f"faces differ in size: {sorted(sizes)}")

    with open(out_path, "wb") as fh:
        fh.write(build_header(faces[0]))
        for face in faces:
            fh.write(face[DDS_HEADER_SIZE:])


if __name__ == "__main__":
    main(sys.argv)
