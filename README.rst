==============
Assets Masters
==============

This repository contains the master artwork for the game *Vega Strike: Upon the Coldest Sea*.

This page describes generic requirements for art work submissions. The submission should happen 
without compression, preferably in higher resolution than what will be used in-game to provide 
for future reuse.

Licenses
--------
Please bear in mind that we are bound to accept contributions under the following licenses. 
This means that if you submit your work for use in Vega Strike, it will be automatically
licensed under GPL unless you state one of the other licenses:

- (GPL) GNU General Public License
- (LGPL) GNU Lesser General Public License
- (GPDL) GNU General Public Documentation License
- (PD) Public Domain
- (CC-BY) Creative Commons By Attribution license
- (CC-SA) Creative Commons Share Alike license
- (CC-BY-SA) Creative Commons By Attribution Share Alike license

Please note that we do not allow licenses not mentioned above, in particular:

- (CC-NC) Creative Commons Non-Commercial license or any combination with CC-BY and CC-SA

What this means is that, besides the licensing of your work, you need to submit/share the source 
files, and in terms of artwork, the master/project files for your contributions. If you are not 
willing to contribute under one of the accepted licenses then please refrain from contributing.

Image types
-----------

For completeness purposes, the following graphics files are being referred to on this page.

**Textures**

- Unit textures
- Cockpit mesh textures
- Planet textures

**Images**

- Base/planet background images
- HUD images (cockpit, shield, armor, ships, gauges, ...)
- Main menu images
- Interface images
- Cargo images
- Space backgrounds
- Animation images

Graphic Files Requirements
--------------------------

Overview of Graphics Requirements
*********************************

When submitting textures, please mind the following requirements for successful inclusion in 
the game:

- Ratio (horizontal:vertical): depending on specific image type (1:1, 2:1, 4:1)
- Dimensions: following the POT rule (power-of-two), size depending on specific image type
- Codec: dds with compression type DXT1 (opaque only), DXT1a, DXT3, or DXT5 (with transparency)
- Extension: .texture for **textures** and .image for **images** (pre-DDS naming png, jpg, 
bmp still may be found in data)
- Quality: RQ or CQ
- Mipmaps: required for **textures**, not required for 2d **images**
- Tileable (seamless): for some image types

Image ratio
***********

The **image ratio** horizontal:vertical will depend on the image type. The recommendations 
are always assuming that pixel ratio is 1:1. This means, no matter what image ratio is used, 
a circle must show as a circle when viewing the image in an image viewer.

For example, it's 2:1 for planet textures, 1:1 for cargo images, planet hud images and 
space background faces, 4:1 for current shield and armor face images.

Square things make sense to be 1:1, however other things can be pretty arbitrary, usually 
you need to round to obtain the closest power of two, for example 400x300 -> 512x256.

Image dimensions
****************

The vertical and horizontal size of the image should be a **power of two** (POT). Really, 
non-POT (non-power-of-two) textures are troublesome, time and memory consuming, since
otherwise they need to be scaled when loaded and it's just best to skip that step. It'd 
be ideal if they were also power of two in *Assets-Masters*, but that's not required, 
but the exports *Assets-Production* should always be some power of 2.

Just use POT. Love the POT. The POT is the mother, the POT is the father. Trust the POT.

That leaves few options for the horizontal or vertical resolution:

- 64 px
- 128 px
- 256 px
- 512 px
- 1024 px
- 2048 px
- 4096 px

1x1 images are allowed, for example if using a texture with a single color, or a 
transparent image.

The size recommendation will depend on the image type. Please refer to the specific 
image type requirements in the `art-related development section <https://wiki.vega-strike.org/Development>`_.

Keeping original high resolution image (e.g. 2048 or 4096 px) versions in stock 
(and in this repository) helps maintaining quality and scalability as game development
progresses or typical screen resolutions rise in the future with better hardware 
available to the players. Also, keeping original 3D-models in stock provides for 
unplanned future changes.

Some images in here are more than 20 years old and in resolutions greater than 2048 px, 
this means we can still use them today. **Kudos to the original artists for their foresight 
and dedication to quality.**

Image Compression Codec
***********************

The graphics format for the production assets of the game is the **dds** format, the
actual file extensions used can be found in `Image Naming (Extension)`_. The source 
images in this repository are not compressed, and should be saved as **png** (preferred 
as it is lossless). For historical reasons you will find **jpg** and **bmp** files within 
the repository, but they are no longer accepted for new submissions.

The minimum texture that is DDS compressed is something like 64x for it to be 
beneficial as far as speed and size are concerned. Anything smaller than that may 
be better off being png, as it won't be compressed anyway.

Allowed compression types are:

- DXT1 for opaque, non alpha layered images only (no transparency).
- DXT1a for 1 bit alpha layered images. (alpha has only black masking, not shades 
of grey; simply: parts of the image have full transparency or are completely opaque).
- DXT3 for semi-transparent images where the transparent layer values are distinct 
(if the alpha is the same shade across the image, or only varies in chunks).
- DXT5 for transparent or semi-transparent images (that are translucent and if the 
translucence varies a lot but not distinctly).

Further clarification: DXT1 is used when the image has no transparent parts at all. 
DXT1a (DXT1 with alpha channel) is used when the image's alpha layer is just 1 value. 
It's either on or off. If it's off, we should remove the alpha layer from the master 
and compress with regular DXT1. DXT3 is used if the image has an alpha layer with 
values other than 0 and 100% but they are not close together. DXT5 takes the same 
amount of space but it interpolates the alpha layer, for smooth
transitions between values.

Mipmaps
*******
It is recommended to create the following images without mipmaps (sequences of 
pre-calculated, optimized images that accompany a main texture) as they do not
need to be scaled down in the game:

- HUD images (cockpit, shield, armor, ships, gauges, ...)
- Main menu images
- Cargo images
- Interface images
- Space backgrounds

While these image types require mipmaps:

- Unit textures
- Cockpit mesh textures
- Animation images
- Planet textures

In case of doubt please ask one of the developers or on the forum.

Compression for production
**************************

Historically the maintainers used the *nvcompress* tool for compressing 
textures to dds format. While a few years have passed since the last update 
of this page, the tool seems to still be around - good for us!

This is the link between this repository and the `production repository 
<https://github.com/vegastrike/Assets-Production>`_ which has the compressed 
textures used in the game in a mirrored folder structure.

Please note that nvcompress (all versions) is invisibly
corrupting DXT5 compressed textures for older nVidia graphic
cards principally with drivers before version 169.09. Please
update to the latest drivers for testing dds textures.

You will need nVidia's free texture tool nvcompress to
transform your original textures to optimized dds textures. Get
the tool here: `NVIDIA Texture Tools 
<http://developer.nvidia.com/object/texture_tools.html>`_

Transform your original texture using nvcompress using one of
the recommended DXT1, DXT1a, DXT3, or DXT5 formats including or
excluding mipmaps (option -nomips).

For DXT1 (opaque) images:

``nvcompress -bc1 (-nomips) texture_original.png texture_dds.texture``

For DXT1a images with transparency:

``nvcompress -bc1 -rgb (-nomips) texture_original.png texture_dds.image``

For DXT3 images with transparency:

``nvcompress -bc2 (-nomips) texture_original.png texture_dds.image``

For DXT5 images with smooth transparency gradient:

``nvcompress -bc3 (-nomips) texture_original.png texture_dds.image``


*Compression with Gimp dds plugin*

Gimp plugin produces dds images with lower quality than hose produced by 
the nvcompress tool. In addition, the plugin uses hardware compression and 
may produce different results on different systems. Therefore, compressing 
images with this plugin is not recommended for submission, but can be used as an
alternative method for local testing purposes only.

*Validation and Testing*

Verify the optimized texture either by opening it with GIMP (with gimp-dds 
plugin installed) and making sure that all mipmap layers (e.g. 12 layers 
for 2048x2048 original image resolution) are contained in the file, or by 
checking it with:

``nvddsinfo texture_dds.texture``

It is strongly recommended to actually test the texture or image in game 
before submitting.

Image Naming (Extension)
************************

Until version 0.5.0 there were codec extensions being used for graphic files 
(**png**, **jpg**, or **bmp**). Unfortunately they have become totally mixed 
up and with the transition to DDS compressed files we have decided to move 
the extensions to codec-independent naming. The reason for having 2 different
extensions was to help artists stick to the requirements by making them aware 
that there is a difference between those 2 extensions. Please note that 
extensions are hard-coded in some cases, so arbitrary interchange might break 
the game's graphics

The following generic, codec independent extensions will be used for graphic files:

- **.image** - for mipmap-less 2d images (backgrounds, ui, cargo, bases, hud images 
and gauges, comm animations, splash screens, ...)
- **.texture** - for textures (unit textures, planet and sun textures, planet rings, 
sun flares, explosions, blinking lights, warp animations, engine trails, nebulae, ...)
- **.cube** - for cube maps (space backgrounds)

The difference between .image and .texture is **only** in the *presence* of mipmaps in 
*.texture* files and *absence* of mipmaps in *.image* files. There is no relation 
whatsoever to directories but depends only on how the graphic files are being used.
The animation directory has subdirectories that have either 2d images or 3d textures. 
The correct naming has to be evaluated for each new file.

Artistic Image Quality
**********************

Committed textures are classified as:

- DQ - Development Quality: textures with very low horizontal resolution and 
low degree of artistic quality
- RQ - Release Quality: textures with at least medium horizontal resolution and 
medium to high degree of artistic quality
- CQ - Cinematographic Quality: textures with high horizontal resolution and 
very high degree of artistic quality

Specific resolution requirements can be found on the `development pages specific to 
each image type <https://wiki.vega-strike.org/Development>`_.

Git Repository Structure
------------------------

There are two repositories for graphics data which are linked together:

- *Assets-Production* (formerly *data*) which holds the compressed/optimized dds images
- *Assets-Masters* (formerly *masters*) which holds the original (png) hi-resolution image
masters plus optionally the source/project files that were used to create the 
compressed images. No other, unrelated files will be kept in *Assets-Masters* (text, data, sprite files, ...).

Further, the following rules apply to **Assets-Masters (aka this repository)**:

- only original uncompressed images go here
- they must be placed in the same (relative) directory as in the compressed images 
in *Assets-Production* 
- the original images must have the same name as those in *Assets-Production*
- Source or project files (.xcf, .blender, ....) are placed in a subdirectory of 
the original image directory called ``sources``. For example, if the original image is 
in ``sprites/planets/earth/earth_texture.png``, the source file should be in 
``sprites/planets/earth/sources/earth_texture.xcf``. This is to keep the source files 
organized and easily identifiable as related to the original image. The source files 
must have the same name as the original.

The following naming convention applies for source files:

- instructions file naming: ``imagefile_instructions.txt``
- copyright/copyleft information should go into: ``imagefile_license.txt``
- source/project file naming: *Source images should be* ``imagefile_source.xcf`` 
    *(or whatever extension)*

The Selection and Vetting Process
---------------------------------

When submitting new art, it is recommended to request feedback from the community 
through the forum before submitting the images or textures. Before you start your work, please check the `art guidelines for the various factions_<https://wiki.vega-strike.org/Art_Guidelines>`.

The following steps are only required when you are **replacing existing art** which 
is already of exceptionally high (cinematographic) quality. If the image/texture 
that you have created meets the texture requirements, then:

- Open a poll for a reasonable period of time (e.g. 1-2 weeks) and describe:
    - which image(s)/texture(s) you'd like to replace; display your candidates
    - briefly describe the method of creation and tools used
    - If you'd like to replace more than one image/texture, describe how you would assign the favorites of the poll to the individual images/textures

- After a set period of time
    - announce the winners
    - and call the poll closed

For both, submitting **replacement of existing art** or **adding missing art** 
(provided the new images/textures are not way off-topic):

**Once there is a winner, submit a PR with the textures in this repository 
(not in Assets-Production)**


References
----------

External:

- `Power of two <http://en.wikipedia.org/wiki/Power_of_two>`_
- `S3 Texture Compression <http://en.wikipedia.org/wiki/S3_Texture_Compression>`_

Forum:

- `Artwork/data overhauls <https://forums.vega-strike.org/viewforum.php?f=28>`_
- `In-game graphics artifacts/errors <https://forums.vega-strike.org/viewforum.php?f=27>`_


Thank you for your dedication to this project to the original Author of the  wiki page `Pyramid3d <https://github.com/pyramid3d>`_!


Folder Structure
----------------

The artwork for the game is divided up into various types. Each section below covers one type of artwork.

All images will require compression to the dds format for production using the ``nvcompress`` tool for publication to production, see `Compression for production`_ for more information.

animations
**********

Animated Images

Each folder is an animated image set. A complete animation consists of:
- The source image data
- A series of PNGs to perform the animation
- An ANI text file with the order of the images for the animation.

The name of the folder matches the name of the ANI file. The ANI file is a text file with the following format:

``-10 10``

``150 .01``

``name0000.texture``

``name0001.texture``

``name0002.texture``    

``name0003.texture``

``...``


The first line are coordinate offsets, in our case that means to offset the texture animation by 10 pixels around the entity's position.

The second line is the number of frames and the time between frames in seconds.

The frames are created by the artist and are named in a sequence with the name of the ANI file as prefix, then commited to this repository.

To publish the frames to production, the following command is used per frame:

``nvcompress -bc1 -nomips name0000.png name0000.texture``

Some animation have transparency and need to use ``-bc3`` instead of ``-bc1``, see `Compression for production`_ for more information.


*NOTE: Not all folders have an ANI file. More information is needed for that use-case.*

cockpits
********

Various parts of the Cockpit display for different types of ships.
Each folder represents a class of ship and contains various elements for the display
of shields, engines, etc.

See `the wiki page <https://wiki.vega-strike.org/Cockpits>`_ for more information on the cockpit file formats, the production images need to be compressed to the ``.dds`` format using the ``nvcompress`` tool, see `Compression for production`_ for more information..

communications
**************

Sounds, Scripts, and Communications for various parts of the game play and story line.

documentation
*************

Written documentation on the game play for user manuals.

To create the manual from the source ``.tex`` file, use the following command:

``pdflatex VSPlayersGuide.tex``

Install LaTex on Ubuntu with the following command:

``sudo apt-get install texlive-full``

logo
****

The Vega Strike logos.

meshes
******

The meshes folder contains the 3D models for the game. The meshes are in the ``.bfxm`` format in production, which is a binary format used by Vega Strike. The source files for the meshes are in the ``.obj`` format, which is the Wavefront OBJ file format.

It is possible to convert between the two formats using the ``vega-meshtool`` command line tool. For example, to convert a BFXM file to an OBJ file, use the following command:

``vega-meshtool --input laser.bfxm --output laser.obj --convert BFXM Wavefront create``

This file can now be opened (or better imported) in Blender or other 3D modeling software for editing. If you want to re-render the model you will need to add proper lighting and camera settings. The template file ``units/vessels/hud_render_template.blend`` can be used for this purpose, it was specifically createdto to re-render the HUD images for the ships but could be adopted for other use cases.

In case you would like to contribute improvements to the 3D models you can modify the model in Blender and then export it back to the OBJ format using Blender's built-in wavefront OBJ exporter. After that you can convert it back to BFXM format using the ``vega-meshtool`` command line tool.

``vega-meshtool --input laser.obj --output laser.bfxm --convert Wavefront BFXM create``

The images for the textures are in the ``.png`` or ``.jpg`` format and need to be compressed to the ``.dds`` format for production using the ``nvcompress`` tool, see `Compression for production`_ for more information. The textures are then referenced in the BFXM file and will be loaded by the game engine. **The image extension needs to stay the same in this case unlike for sprites and regular textures (this may change in future releases).**

*Note: Not all conversion paths are supported, bfxm <-> obj has been verified and works.*

sounds
******

Various sounds for the game play.

sprites
*******

The sprites folder contains image work for interface display parts - bases, HUD images of planets, common flight parts, etc.

The sprites should ideally be in high resolution (e.g. 2048x2048 for bases) and then compressed to the dds format for production using the ``nvcompress`` tool, see `Compression for production`_ for more information. The target extension is ``.image``.

**Bases**

Each base has a folder with a set of images for various views of the base, in most cases as a minimum:

- the landing pad / hangar
- the main concourse
- the bar
- the trade room
- the ship dealer

Those images can be improved and upgraded by artists, if you would like to create new bases or addtional rooms to existing bases please contact the developers on the forum first to discuss your ideas.

The production repostory has a bases folder with python files for each base, this is where the textures are loaded and the interaction areas are defined.

**HUD Images for Planets**

The HUD images for planets are generated using POV-Ray and the POV-Ray scene files are in the ``sprites/sources`` folder. 

textures
********

Image work for textures of various objects (see folder names), for the most part they can be modified, saved and then compressed to the ``.dds`` format for production using the ``nvcompress`` tool, see `Compression for production`_ for more information.

**galaxy backgrounds**

A special case are the galaxy background images, they are in the ``.cube`` format and are used for the space backgrounds. The source images are in the ``.png`` format and need to be compressed to the ``.dds`` format using the ``nvcompress`` tool and then assembled via ``nvassemble`` for production. The easiest way to achieve this is via ``scripts/build``. In case you would like to manually assemble the cube, the proper face order is:

- left
- right
- front
- back
- up (rotated 90 degrees clockwise)
- down (rotated 180 degrees)

The tool ``scripts/galaxy_viewer-py`` can be used to view the galaxy background images in the ``.cube`` format without starting the game, it allows side-by-side comparison as well to quickly compare different versions.

units
*****

The units folder contains the 3D models for the ships and other units in the game (this is not true for all units). See `meshes`_ for more information on the 3D models and their textures. Key folders are:

- cargo - the 3D model of ejected cargo in space, can be picked up by the player
- eject - the 3D model of ejected pilots in space
- equipment - only contain "mobile battery platform"
- factions - is this still used?
- installations - the 3D models of the bases (planets are handled differently)
- landscape - is this still used?
- subunits - the 3D models of the subunits (e.g. turrets) of the ships
- vessels - the 3D models of the ships, probably most relevant
- weapons - the 3D models of the weapons (e.g. missiles, torpedoes, etc.), currently no source files, see `How to make a new weapon_<https://wiki.vega-strike.org/HowTo:Make_Weapons>`` for more information
- wormhold - the 3d model of the wormhole

In most cases the 3D model file (mesh) is missing and needs to be converted from the BFXM format to the OBJ format using the ``vega-meshtool`` command line tool. See `meshes`_ for more information.

Converting Masters to Production
--------------------------------

The ``scripts/build`` script can be used to convert the master images to production images. It will compress the images to the dds format using the ``nvcompress`` tool with the proper settings and assemble the galaxy background images via ``nvassemble``. The script will publish the compressed images to a build folder which can then be used to update the production repository.

The ``scripts/bootstrap`` script can be used to install the required tools for the build process on Linux and MacOS.