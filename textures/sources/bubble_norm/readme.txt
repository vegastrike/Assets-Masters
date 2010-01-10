Note to whoever:
Please port this readme.txt to the wiki as a Tileable Normalmap Tutorial.
I cannot edit the wiki anymore, as it doesn't like the fact tha "chuck_starchaser"
has an underscore in it...
The reason this is here is that the three blender files provided are the sources
for the bubble_norm.texture file, and could be used as they are or modified for
similar purposes. The only image file needed as input is NOT provided, simply
because all it contains is noise, and would take up three megs in the repository;
so instructions on how to produce the noise are provided instead. See below.

A Tileable Normalmap Tutorial
=============================

The "bubble_norm.texture" normalmap is intended as a generic, tiling normalmap
that produces a wobbly surface similar to what you see in very old glass panes.
(Science note: Glass is a very high viscosity liquid, rather than a solid. It
sort of "melts" down gradually over decades and centuries.)
Generating such a normalmap is not trivial, and therefore these sources and this
file are here as a case study.

Considerations:

a) Consistency
Randomizing the normals would NOT achieve a good result. It would produce perceivable
inconsistencies, as the normals in one axis may suggest a bump, at a given place, but
the normals in the other axis might say there's a depression there. For natural-looking
bumpiness you need the normals to produce a consistent illusion. To achieve that, we
must produce a height map first, and from it generate our normals.

b) Value Quantization
The quantization artifacts of 8-bit encoding are bad enough. With DXT compression we
get 8-bits for the alpha channel, but only 5-6-5 bits for the RGB channels.
It is therefore imperative to try and use as many of those bits as possible, to get
normals with some continuity. We will therefore produce an exaggerated normalmap, and
reduce its strength later, in the shader, at GPU's internal floating point precision.
For encoding, we will use the CineMut normalmap encoding standard: UUUV, wherebay the
dU channel is put in all 3 RGB channels with offsets to reduce quantization, and the
dV channel is sent to the 8-bit precision alpha channel.
The offsets for dU are positive 0.01 for the red channel, and negative 0.01 for the
blue channel. This causes the three channels to switch numbers in staggered fashion,
so that when added together in the shader we get up to 7-bits of resolution.
The Z channel is not encoded, in this format, as it can be recovered in the shader by
filling in a fixed value for Z, and then using normalize().

c) Texture space quantization
Complementary to consistency, one must consider the inconsistency artifacts resulting
from trying to pack more normal data information per texel than is wise. It is common
in digital signal processing to speak of the Nyquist limit of 1/2 of the sampling
frequency for encoded data. At 44 KHz sampling, the Nyquist limit would be 22 KHz.
The Nyquist limit is not terribly conservative, however; and studio sampling of audio
data is done at 180 KHz. Thus, our height map bumps should be rounded from random noise
by using a blur radius of 4 texels at the final texture size. But our master texture
size will be twice the final, so our blur radius would be 8. However, I prefer to use
odd radii for blurs. What we will do is apply one pass of radius 9, and then apply
successive blur passes with radius 7, 5 and 3 in a Blender noodle, at full precision.

d) Tileability
Blender doesn't have lileable blur filters in its node system; but there is a very
simple way to make our normalmap tileable: Begin by creating a noise pattern at 512,
copy and paste it four times into a 1024 texture, then apply all the filters and the
normalmap conversion and reduction, and then simply cut a square half the size from
somewhere near the middle of the texture. Doesn't have to come from the exact center,
as long as it's not from too close to an edge. Try it, if you don't believe me ;-)


Steps to achievement:

1) In Gimp, create a 512 x 512 texture.

2) From Filters -> Noise -> RGB noise, sliders at max; uncorrelated, independent.
Notes: To obtain the most data for Blender's higher precision processing, we use
uncorrelated, independent (colorful) noise, giving us 9.5 bits-worth of data per
texel.

3) Squint the eyes, and Hit CTRL-F repeatedly until a pattern appears that doesn't
look like it has any noticeable spots or singularities.

4) Save the file, just in case; then A (select All), and CTRL-C, for copy.

5) Double the canvas size to 1024 x 1024, then Flatten Image.

6) CTRL-V for Paste four times, each time placing the pasted layer against one of
the four corners exactly. Save the file as "noise.tga", un-compressed.
Notes: Why un-compressed? Because it is completely random noise, which is not
compressible by definition, except in lossy ways, which we don't want. This is a
temporary file that we can delete once we are finished.

7) Start Blender, make your main window a Node Editor window, click on the face
icon, then on Use Nodes, then un-click Use Nodes, and delete the two nodes that
appeared there. Then create a network for blurring, or use the file included in
this folder: blur_stage.blend. Be sure to write an EXR as the output format.
This stage also amplifies the height data, but applies an arctan function to
squeeze the bumps, so they look a bit flattened, rather than like rolling hills;
then computes normals.
The file created is bump_height0001.exr, and can only be viewed in Blender or
using a special EXR viewer, as it's a 64-bit per channel precision image format.

8) Roll your own, or use the normal_stage.blend network to create a normalmap.
Writes a file named uuuv_normal0001.exr in our proprietary UUUV format :)

9) Roll your own, or use the reduce_and_cut_stage.blend network provided to
reduce the size to 512, and then crop a 256 x 256 chunk from the middle.
Writes a final file named bubble_norm0001.png.

10) Use nvcompress to compress the image with DXT5, add mipmaps and save it as
a dds format image. The command line is,
           nvcompress -bc3 -nocuda bubble_norm0001.png
Saves a file named "bubble_norm0001.dds".

11) Rename the file to "bubble_norm.texture".
