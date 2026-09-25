=============================
Background rendering (POV-Ray)
=============================

Render the Vega Strike space backgrounds from their POV-Ray sources and
assemble the compressed DDS cubemaps the engine loads. The sources live in
``textures/backgrounds/sources/`` as ``<name>_source.zip``; this directory
turns one into ``build/backgrounds/<name>_light.cube``.

Eight backgrounds have a POV-Ray source. The other backgrounds in
``textures/backgrounds/`` are pre-rendered faces whose render source is not in
this repository.

Required programs
=================

- **POV-Ray 3.7** — renders the six skybox frames.

  - Arch: ``povray``; Ubuntu/Debian: ``povray``; macOS: ``brew install povray``.
  - The sources ``#include "rand.inc"``, which ships with POV-Ray, not with the
    zip. The script adds the stock include directory to the search path
    automatically; set ``POV_STOCK_INC`` if it is somewhere unusual.

- **ImageMagick** (the ``magick`` command) — rotates each frame to the face
  orientation and writes DXT1 DDS with a full mip chain.

- **Python 3** — runs ``dds_cubemap.py``, which concatenates the six face DDS
  files into a cubemap. No tool does both DXT1 and cubemaps: ImageMagick writes
  DXT1 but only flat 2D, and cmft writes cubemaps but cannot compress.

Usage
=====

.. code-block:: sh

    scripts/povray/render-backgrounds.sh                 # every sourced background
    scripts/povray/render-backgrounds.sh red_galaxy1     # one of them
    RES=4096 scripts/povray/render-backgrounds.sh starfield

``RES`` defaults to 1024, the resolution the shipped cubemaps use. 4096 is
where this becomes useful for modern displays (and takes a great deal longer).

Rendering writes only to ``build/`` (gitignored); nothing is added to the
repository. To use a cubemap in the game, back up the shipped
``Assets-Production/textures/backgrounds/<name>_light.cube``, copy the rendered
one over it, and raise ``graphics.max_cubemap_size`` in ``engine.json`` above
1024 if you rendered larger than that.

The pipeline
============

1. **Render** the source's six frames with its skybox camera (``CAMERA = 6``)
   at ``RES`` x ``RES``.
2. **Map frames to DDS faces.** The mapping is fixed, and the up and down faces
   additionally need a rotation to match Vega Strike's orientation:

   =========  =========  ========
   DDS face   POV frame  rotation
   =========  =========  ========
   +X         4          0
   -X         2          0
   +Y         5          90
   -Y         6          180
   +Z         3          0
   -Z         1          0
   =========  =========  ========

   This was verified against the shipped ``starfield_light.cube``: the
   assembled file is byte-size identical and each face matches within RMSE
   ~0.02.
3. **Compress** each face to DXT1 DDS with a full mip chain (ImageMagick).
4. **Assemble** the six faces into a cubemap DDS (``dds_cubemap.py``).

Target format
=============

The engine loads ``textures/backgrounds/<name>_light.cube``:

- DXT1 (DDS), six faces, full mip chain.
- ``engine/src/gfx/vsimage.cpp ReadDDS()`` accepts **only DXT1/DXT3/DXT5** — an
  uncompressed DDS is rejected.
- Face order in the file is the standard DDS cubemap order: +X, -X, +Y, -Y,
  +Z, -Z.
- ``graphics.max_cubemap_size`` (default 1024) clamps the size at load time.

Source zips
===========

These zips come from Pyramid's `Space3D <http://space3d.no.sapo.pt/>`_ (2008)
and are GPL. They are not all self-contained:

=================  =====  ==================  ====================
name               scene  ships its includes  notes
=================  =====  ==================  ====================
``starfield``      34     ``starfield.inc``   —
``starfield2``     36     ``starfield.inc``   —
``starfield3``     37     ``starfield.inc``   its ini starts at frame 2
``starfield4``     39     ``starfield.inc``   its ini starts at frame 2
``starfield5``     41     both                heavy (~12 h at 4096)
``plasma_galaxy``  32     both                —
``milkyway``       33     ``starfield.inc``   needs ``hipp8.tiff`` (see below)
``red_galaxy1``    31     neither (see fixups)
=================  =====  ==================  ====================

The script handles the common gaps:

- A zip missing ``starfield.inc`` or ``spiral_galaxy.inc`` borrows it from a
  sibling source (``DONOR``, default ``starfield5``).
- An ini that starts at frame 2 is overridden with ``+SF1 +EF6``, so all six
  faces are rendered.

``milkyway``
------------

Its scene is an ``image_map { tiff "hipp8.tiff" }`` sky sphere, and the zip does
not carry that image. It is a third-party star catalogue image and is **not
redistributed here**. Put a copy in a directory and point ``POV_EXTRA`` at it:

.. code-block:: sh

    POV_EXTRA=~/povray-extras scripts/povray/render-backgrounds.sh milkyway

``red_galaxy1``
---------------

Its zip ships no ``starfield.inc`` between the two, and its scene is written
against the **pre-0.17** Space3D API. Space3D v0.17 (2008-04-10) was "a
complete rework of pigments and objects to macros": the parallel-object macros
(``mCloudNebula(colors, shape, rng)``) became the ``mNebulaSelect(...)``
selector, and the pigments and objects became no-argument macros. None of the
includes in this repository predate that rework.

``fixups/red_galaxy1/starfield_example.pov`` is the same scene with scene 31
ported to the current API; the script applies it over the zip's copy. The port
is:

- ``mCloudNebula(NEBULA_COLORS, rShape, rColor)`` → ``mNebulaSelect(1, n, 1,
  NEBULA_COLORS, 0, rShape, rColor)`` (cloud nebula variants 1 and 2, the two
  dense cloud objects the scene places);
- ``O_StarCluster05`` and ``P_StarField05`` → ``O_StarCluster05(1, rPosition)``
  and ``P_StarField05()`` (the no-argument macro forms; ``O_StarCluster05``
  gained a distribution method and a seed at v0.18).

Everything else in the scene — the star-cluster globals
(``starcluster_excentricity``, ``starcluster_rotation``,
``starfield_star_amount``, ...) and the objects that read them — carries over
unchanged, because the newer include still reads those globals.

The result is a red nebula in the right family but **not pixel-identical to the
shipped art**: the v0.16 nebula objects are gone, so the two clouds are a
different pair. Rendering the shipped look faithfully would need the original
v0.16 ``starfield.inc`` / ``spiral_galaxy.inc``, which nobody has found locally.

Adding a background
===================

Add ``textures/backgrounds/sources/<name>_source.zip`` and, if the scene needs
patching, ``fixups/<name>/`` with the patched files. The script picks it up by
name; there is nothing to register. Sources that are still authored against the
old API should be ported the way ``red_galaxy1`` was.

Credits
=======

The POV-Ray scenes are Pyramid's Space3D. The spiral galaxy macro is Tekno
Frannansa's; the nebula object is Jaime Vives Piqueres'.
