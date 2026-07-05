#!/usr/bin/env python3
# # /// script
# dependencies = [
#   "pillow>=10.4.0",
# ]
# ///
#====================================
# @file   : cropandresize
# @brief  : Python script for to crop an image to an object and scale it to a certain resolution
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
import os
import argparse
from PIL import Image, ImageChops, ImageFile, ImageOps
ImageFile.LOAD_TRUNCATED_IMAGES = True

def process_images_in_folder(folder_path, target_size):
    # Iterate through all files in the directory
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            file_path = os.path.join(folder_path, filename)
            
            with Image.open(file_path) as img:
                # 1. Find the bounding box of non-transparent content
                bg = Image.new(img.mode, img.size, (0, 0, 0, 0))
                diff = ImageChops.difference(img, bg)
                diff = ImageChops.add(diff, diff, 2.0, -100)
                bbox = diff.getbbox()
                
                # 2. Crop if content exists
                if bbox:
                    img = img.crop(bbox)
                
                # 3. Downscale using high-quality resampling
                img = ImageOps.contain(img, (target_size, target_size), method=Image.Resampling.LANCZOS)

                # 3.1 Now pad it to get a squared image
                img = ImageOps.pad(img, (target_size, target_size), color=(0, 0, 0, 0), centering=(0.5, 0.5))

                # 4. Save back to the same file path (In-place)
                img.save(file_path)
                print(f"Processed: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crop and resize PNGs in a folder.")
    parser.add_argument("--folder", required=True, help="Path to the folder containing images")
    parser.add_argument("--size", type=int, default=1024, help="Target width/height in pixels")
    #parser.add_argument("--suffix", help="An optional image suffix")
    
    args = parser.parse_args()
    
    process_images_in_folder(args.folder, args.size)