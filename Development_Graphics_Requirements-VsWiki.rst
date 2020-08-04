==========================================
Development:Graphics Requirements - VsWiki
==========================================

.. container:: noprint
   :name: mw-page-base

.. container:: noprint
   :name: mw-head-base

.. container:: mw-body
   :name: content

   .. container::
      :name: mw-js-message

   .. rubric:: Development:Graphics Requirements
      :name: firstHeading
      :class: firstHeading

   .. container::
      :name: bodyContent

      .. container::
         :name: siteSub

         From VsWiki

      .. container::
         :name: contentSub

      .. container:: mw-jump
         :name: jump-to-nav

         Jump to: `navigation <#mw-navigation>`__,
         `search <#p-search>`__

      .. container:: mw-content-ltr
         :name: mw-content-text

         .. container:: toc
            :name: toc

            .. container::
               :name: toctitle

               .. rubric:: Contents
                  :name: contents

            -  `1 Introduction <#Introduction>`__
            -  `2 Licenses <#Licenses>`__
            -  `3 Image Types <#Image_Types>`__
            -  `4 Graphic Files
               Requirements <#Graphic_Files_Requirements>`__

               -  `4.1 Overview of Graphics
                  Requirements <#Overview_of_Graphics_Requirements>`__
               -  `4.2 Image ratio <#Image_ratio>`__
               -  `4.3 Image dimensions <#Image_dimensions>`__
               -  `4.4 Image Compression
                  Codec <#Image_Compression_Codec>`__
               -  `4.5 Mipmaps <#Mipmaps>`__

                  -  `4.5.1 Compression with
                     nvcompress <#Compression_with_nvcompress>`__
                  -  `4.5.2 Compression with Gimp dds
                     plugin <#Compression_with_Gimp_dds_plugin>`__
                  -  `4.5.3 Validation and
                     Testing <#Validation_and_Testing>`__

               -  `4.6 Image Naming
                  (Extension) <#Image_Naming_.28Extension.29>`__
               -  `4.7 Artistic Image
                  Quality <#Artistic_Image_Quality>`__
               -  `4.8 SVN Structure <#SVN_Structure>`__

            -  `5 The Selection and Vetting
               Process <#The_Selection_and_Vetting_Process>`__
            -  `6 See Also (References) <#See_Also_.28References.29>`__

               -  `6.1 Author: pyramid <#Author:_pyramid>`__

         .. rubric:: Introduction
            :name: introduction

         This wiki page describes generic requirements for art work
         submissions. The submission can happen without compression,
         preferably in higher resolution than will be used in-game to
         provide for future extension.

         .. rubric:: Licenses
            :name: licenses

         Please bear in mind that we are bound to accept contributions
         under the following licenses. This means that if you submit
         your work for use in Vega Strike, it will be automatically
         licensed under GPL unless you state one of the other licenses:

         -  (GPL) GNU General Public License
         -  (LGPL) GNU Lesser General Public License
         -  (GPDL) GNU General Public Documentation License
         -  (PD) Public Domain
         -  (CC-BY) Creative Commons By Attribution license
         -  (CC-SA) Creative Commons Share Alike license
         -  (CC-BY-SA) Creative Commons By Attribution Share Alike
            license

         Please note that we do not allow licenses not mentioned above,
         in particular:

         -  (CC-NC) Creative Commons Non-Commercial license or any
            combination with CC-BY and CC-SA

         What this means is that, besides the licensing of your work,
         you need to submit/share the source files, and in terms of
         artwork, the master/project files for your contributions. If
         you are not willing to contribute under one of the accepted
         licenses then simply forget it.

         .. rubric:: Image Types
            :name: image-types

         For completeness purposes, the following graphics files are
         being referred to on this page.

         **Textures**

         -  Unit textures
         -  Cockpit mesh textures
         -  Planet textures

         **Images**

         -  Base/planet background images
         -  HUD images (cockpit, shield, armor, ships, gauges, ...)
         -  Main menu images
         -  Interface images
         -  Cargo images
         -  Space backgrounds
         -  Animation images

         .. rubric:: Graphic Files Requirements
            :name: graphic-files-requirements

         .. rubric:: Overview of Graphics Requirements
            :name: overview-of-graphics-requirements

         Textures ready for submission should fulfill:

         -  Ratio (horizontal:vertical): depending on specific image
            type (1:1, 2:1, 4:1)
         -  Dimensions: following the POT rule (power-of-two), size
            depending on specific image type
         -  Codec: dds with compression type DXT1 (opaque only), DXT1a,
            DXT3, or DXT5 (with transparency)
         -  Extension: .texture for **textures** and .image for
            **images** (pre-DDS naming png, jpg, bmp still may be found
            in data)
         -  Quality: RQ or CQ
         -  Mipmaps: required for **textures**, not required for 2d
            **images**
         -  Tileable (seamless): for some image types

         .. rubric:: Image ratio
            :name: image-ratio

         The **image ratio** horizontal:vertical will depend on the
         image type. The recommendations are always assuming that pixel
         ratio is 1:1. This means, no matter what image ratio is used, a
         circle must show as a circle when viewing the image in an image
         viewer.

         For example, it's 2:1 for planet textures, 1:1 for cargo
         images, planet hud images and space background faces, 4:1 for
         current shield and armor face images.

         Square things make sense to be 1:1, however other things can be
         pretty arbitrary, usually you need to round to obtain the
         closest power of two, for example 400x300 -> 512x256.

         .. rubric:: Image dimensions
            :name: image-dimensions

         The vertical and horizontal size of the image should be a
         **power of two** (POT). Really, non-POT (non-power-of-two)
         textures are troublesome, time and memory consuming, since
         otherwise they need to be scaled when loaded and it's just best
         to skip that step. It'd be ideal if they were also power of two
         in *masters*, but that's not required, but the exports to
         data4.x should always be some power of 2.

         Just use POT. Love the POT. The POT is the mother, the POT is
         the father. Trust the POT.

         That leaves few options for the horizontal or vertical
         resolution:

         -  64 px
         -  128 px
         -  256 px
         -  512 px
         -  1024 px
         -  2048 px

         1x1 images are allowed, for example if using a texture with a
         single color, or a transparent image.

         The size recommendation will depend on the image type. Please
         refer to the specific image type requirements in the
         art-related `Development </Development>`__ section.

         Keeping original high resolution image (e.g. 1024 or 2048)
         versions in stock (and in svn masters directory) helps
         maintaining quality and scalability as game development
         progresses or typical screen resolutions rise in the future
         with better hardware available to the players. Also, keeping
         original 3D-models in stock provides for unplanned future
         changes.

         .. rubric:: Image Compression Codec
            :name: image-compression-codec

         The graphics format for the game is **dds** format, (though the
         file extension can be either **png** (preferred), **jpg**, or
         **bmp**).

         The minimum texture that is DDS compressed is something like
         64x for it to be beneficial as far as speed and size are
         concerned. Anything smaller than that may be better off being
         png, as it won't be compressed anyway.

         Allowed compression types are:

         -  DXT1 for opaque, non alpha layered images only (no
            transparency).
         -  DXT1a for 1 bit alpha layered images. (alpha has only black
            masking, not shades of grey; simply: parts of the image have
            full transparency or are completely opaque).
         -  DXT3 for semi-transparent images where the transparent layer
            values are distinct (if the alpha is the same shade across
            the image, or only varies in chunks).
         -  DXT5 for transparent or semi-transparent images (that are
            translucent and if the translucence varies a lot but not
            distinctly).

         Further clarification: DXT1 is used when the image has no
         transparent parts at all. DXT1a (DXT1 with alpha channel) is
         used when the images alpha layer is just 1 value. It's either
         on or off. If it's off, we should remove the alpha layer from
         the master and compress with regular dxt1. DXT3 is used if the
         image has an alpha layer with values other than 0 and 100% but
         they are not close together. DXT5 takes the same amount of
         space but it interpolates the alpha layer, for smooth
         transitions between values.

         .. rubric:: Mipmaps
            :name: mipmaps

         It is recommended to create the following images without
         mipmaps:

         -  HUD images (cockpit, shield, armor, ships, gauges, ...)
         -  Main menu images
         -  Cargo images
         -  Interface images
         -  Space backgrounds

         While this image types require mipmaps:

         -  Unit textures
         -  Cockpit mesh textures
         -  Animation images
         -  Planet textures

         In case of doubt please ask one of the developers or on the
         forum.

         .. rubric:: Compression with nvcompress
            :name: compression-with-nvcompress

         .. container:: boilerplate metadata
            :name: warning

            Please note that nvcompress (all versions) is invisibly
            corrupting DXT5 compressed textures for older nVidia graphic
            cards principally with drivers before version 169.09. Please
            update to the latest drivers for testing dds textures.

         You will need nVidia's free texture tool nvcompress to
         transform your original textures to optimized dds textures. Get
         the tool here: `NVIDIA Texture
         Tools <http://developer.nvidia.com/object/texture_tools.html>`__

         **Sidenote**: The following applies only to NVIDIA texture
         tools version 0.9.4. More recent versions exist. Due to a bug
         in handling 1 pixel mipmaps in the original (0.9.4) version,
         you will be further required to patch the tools with safemode's
         patch. The patch can be obtained here: `save
         nvidia-texture.patch
         file <http://signal-lost.homeip.net/files/nvidia-texture.patch>`__.
         Patch the texture tools, compile, and install them.

         Transform your original texture using nvcompress using one of
         the recommended DXT1, DXT1a, DXT3, or DXT5 formats including or
         excluding mipmaps (option -nomips).

         For DXT1 (opaque) images:

         -  ``nvcompress -bc1 (-nomips) texture_original.png texture_dds.texture``

         For DXT1a images with transparency:

         -  ``nvcompress -bc1 -rgb (-nomips) texture_original.png texture_dds.image``

         For DXT3 images with transparency:

         -  ``nvcompress -bc2 (-nomips) texture_original.png texture_dds.image``

         For DXT5 images with smooth transparency gradient:

         -  ``nvcompress -bc3 (-nomips) texture_original.png texture_dds.image``

         .. rubric:: Compression with Gimp dds plugin
            :name: compression-with-gimp-dds-plugin

         Gimp plugin produces dds images with lower quality than that
         one produced by the nvcompress tool. In addition, the plugin
         uses hardware compression and may produce different results on
         different systems. Therefore, compressing images with this
         plugin is not recommended for submission, but can be used as an
         alternative method for local testing purposes only.

         .. rubric:: Validation and Testing
            :name: validation-and-testing

         Verify the optimized texture either by opening it with GIMP
         (with gimp-dds plugin installed) and making sure that all
         mipmap layers (e.g. 12 layers for 2048x2048 original image
         resolution) are contained in the file, or by checking it with:

         -  ``nvddsinfo texture_dds.texture``

         It is strongly recommended to actually test the texture or
         image in game before submitting.

         .. rubric:: Image Naming (Extension)
            :name: image-naming-extension

         Until version 0.5.0 there were codec extensions being used for
         graphic files (**png**, **jpg**, or **bmp**). Unfortunately
         they have become totally mixed up and with the transition to
         DDS compressed files we have decided to move the extensions to
         codec-independent naming. The reason for having 2 different
         extensions was to help artists stick to the requirements by
         making them aware that there is a difference between those 2
         extensions. Please note that extensions are coded in some cases
         so arbitrary interchange might break your graphics.

         The following generic, codec independent extensions will be
         used for graphic files:

         -  **.image** - for mipmap-less 2d images (backgrounds, ui,
            cargo, bases, hud images and gauges, comm animations, splash
            screens, ...)
         -  **.texture** - for textures (unit textures, planet and sun
            textures, planet rings, sun flares, explosions, blinking
            lights, warp animations, engine trails, nebulae, ...)

         The difference between .image and .texture is **only** in the
         *presence* of mipmaps in *.texture* files and *absence* mipmaps
         in *.image* files. There is no relation whatsoever to
         directories but depends only on how the graphics is being used.
         The animation directory has subdirectories that have either 2d
         images or 3d textures. The correct naming has to be evaluated
         for each new file.

         .. rubric:: Artistic Image Quality
            :name: artistic-image-quality

         Committed textures are classified as:

         -  DQ - Development Quality: textures with very low horizontal
            resolution and low degree of artistic quality
         -  RQ - Release Quality: textures with at least medium
            horizontal resolution and medium to high degree of artistic
            quality
         -  CQ - Cinematographic Quality: textures with high horizontal
            resolution and very high degree of artistic quality

         Specific resolution requirements can be found on the
         development pages specific to each image type.

         .. rubric:: SVN Structure
            :name: svn-structure

         The subversion (svn) repository has two directories for
         graphics data:

         -  *data* that holds the compressed/optimized dds images
         -  *masters* that holds the original (png) hi-resolution image
            masters plus optionally the source/project files that were
            used to create the compressed images. no other files will be
            kept in masters (text, data, sprite files, ...).

         Further, the following rules apply to **masters**:

         -  only original uncompressed images go here
         -  they must be placed in the same (relative) directory as in
            the compressed images in *data*
         -  the original images must have the same name as those in
            *data*
         -  Source or project files (.xcf, .blender, ....) are placed in
            a subdirectory of the original image directory called
            *sources*
         -  The following naming convention applies for source files:

            -  instructions file naming: *imagefile_instructions.txt*
            -  copyright/copyleft information should go into:
               *imagefile_license.txt*
            -  source/project file naming: *Source images should be*
               imagefile_source.xcf *(or whatever extension)*
            -  if several source files are required to execute the
               project, place them in a zip file

         .. rubric:: The Selection and Vetting Process
            :name: the-selection-and-vetting-process

         When submitting new art, it is recommended to request feedback
         from the community through the forum before submitting the
         images or textures.

         The following steps are only required when you are **replacing
         existing art** which is already of exceptionally high
         (cinematographic) quality. If the image/texture that you have
         created meets the texture requirements, then:

         -  Open a poll for a reasonable period of time (e.g. 1-2 weeks)
            and describe:

            -  which image(s)/texture(s) you'd like to replace
            -  display your candidates
            -  briefly describe the method of creation and tools used
            -  If you'd like to replace more than one image/texture,
               describe how you would assign the favorites of the poll
               to the individual images/textures

         -  After a set period of time

            -  announce the winners
            -  and call the poll closed

         For both, submitting **replacement of existing art** or
         **adding missing art** (provided the new images/textures are
         not way off-topic):

         -  Submit the textures to svn (in case you have commit rights
            attributed), or
         -  through the forum or private message, ask a developer with
            write access to submit them (e.g. the maintainer of this
            page, `pyramid </User:Pyramid>`__).

         .. rubric:: See Also (References)
            :name: see-also-references

         External:

         -  `Power of two <http://en.wikipedia.org/wiki/Power_of_two>`__
         -  `S3 Texture
            Compression <http://en.wikipedia.org/wiki/S3_Texture_Compression>`__

         Forum:

         -  `Artwork/data
            overhauls <http://vegastrike.sourceforge.net/forums/viewtopic.php?p=93665>`__
         -  `GL graphics
            artifacts/errors <http://vegastrike.sourceforge.net/forums/viewtopic.php?p=93658>`__
         -  `image format
            issues <http://vegastrike.sourceforge.net/forums/viewtopic.php?t=10585>`__
         -  `graphics size in
            data4.x <http://vegastrike.sourceforge.net/forums/viewtopic.php?t=10582>`__

         | 

         .. rubric:: Author:\ `pyramid </User:Pyramid>`__
            :name: author-pyramid

      .. container:: printfooter

         Retrieved from
         "https://wiki.vega-strike.org/mediawiki/index.php?title=Development:Graphics_Requirements&oldid=18176"

      .. container:: catlinks
         :name: catlinks

         .. container:: mw-normal-catlinks
            :name: mw-normal-catlinks

            `Category </Special:Categories>`__:

            -  `Development </Category:Development>`__

      .. container:: visualClear

.. container::
   :name: mw-navigation

   .. rubric:: Navigation menu
      :name: navigation-menu

   .. container::
      :name: mw-head

      .. container::
         :name: p-personal

         .. rubric:: Personal tools
            :name: p-personal-label

         -  `Log
            in </mediawiki/index.php?title=Special:UserLogin&returnto=Development%3AGraphics+Requirements>`__

      .. container::
         :name: left-navigation

         .. container:: vectorTabs
            :name: p-namespaces

            .. rubric:: Namespaces
               :name: p-namespaces-label

            -  `Page </Development:Graphics_Requirements>`__
            -  `Discussion </mediawiki/index.php?title=Talk:Development:Graphics_Requirements&action=edit&redlink=1>`__

         .. container:: vectorMenu emptyPortlet
            :name: p-variants

            .. rubric:: 
               :name: mw-vector-current-variant

            .. rubric:: Variants\ ` <#>`__
               :name: p-variants-label

            .. container:: menu

      .. container::
         :name: right-navigation

         .. container:: vectorTabs
            :name: p-views

            .. rubric:: Views
               :name: p-views-label

            -  `Read </Development:Graphics_Requirements>`__
            -  `View
               source </mediawiki/index.php?title=Development:Graphics_Requirements&action=edit>`__
            -  `View
               history </mediawiki/index.php?title=Development:Graphics_Requirements&action=history>`__

         .. container:: vectorMenu emptyPortlet
            :name: p-cactions

            .. rubric:: Actions\ ` <#>`__
               :name: p-cactions-label

            .. container:: menu

         .. container::
            :name: p-search

            .. rubric:: Search
               :name: search

            .. container::
               :name: simpleSearch

               |Search|

   .. container::
      :name: mw-panel

      .. container::
         :name: p-logo

         ` </Main_Page>`__

      .. container:: portal
         :name: p-navigation

         .. rubric:: Navigation
            :name: p-navigation-label

         .. container:: body

            -  `Main page </Main_Page>`__
            -  `Recent changes </Special:RecentChanges>`__
            -  `Random page </Special:Random>`__
            -  `Help <https://www.mediawiki.org/wiki/Special:MyLanguage/Help:Contents>`__

      .. container:: portal
         :name: p-tb

         .. rubric:: Tools
            :name: p-tb-label

         .. container:: body

            -  `What links
               here </Special:WhatLinksHere/Development:Graphics_Requirements>`__
            -  `Related
               changes </Special:RecentChangesLinked/Development:Graphics_Requirements>`__
            -  `Special pages </Special:SpecialPages>`__
            -  `Printable
               version </mediawiki/index.php?title=Development:Graphics_Requirements&printable=yes>`__
            -  `Permanent
               link </mediawiki/index.php?title=Development:Graphics_Requirements&oldid=18176>`__
            -  `Page
               information </mediawiki/index.php?title=Development:Graphics_Requirements&action=info>`__

.. container::
   :name: footer

   -  This page was last modified on 1 April 2011, at 21:53.
   -  This page has been accessed 9,128 times.
   -  Content is available under\ `GNU Free Documentation License
      1.2 <http://www.gnu.org/copyleft/fdl.html>`__\ unless otherwise
      noted.

   -  `Privacy policy </VsWiki:Privacy_policy>`__
   -  `About VsWiki </VsWiki:About>`__
   -  `Disclaimers </VsWiki:General_disclaimer>`__

   -  |GNU Free Documentation License 1.2|
   -  |Powered by MediaWiki|

   .. container::

.. |Search| image:: /mediawiki/skins/vector/images/search-ltr.png?303
   :width: 12px
   :height: 13px
.. |GNU Free Documentation License 1.2| image:: /mediawiki/skins/common/images/gnu-fdl.png
   :width: 88px
   :height: 31px
   :target: http://www.gnu.org/copyleft/fdl.html
.. |Powered by MediaWiki| image:: /mediawiki/skins/common/images/poweredby_mediawiki_88x31.png
   :width: 88px
   :height: 31px
   :target: //www.mediawiki.org/
