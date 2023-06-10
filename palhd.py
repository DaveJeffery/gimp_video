#!/usr/bin/env python

#   The GIMP PAL plugin - PAL effect plugin for The GIMP.
#   Copyright (C) 2009  Dave Jeffery <david.richard.jeffery@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gimpfu import *

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)

# Constants definitions
PAL_S = 1.0
PAL_D = 0.5

def palhd(img, layer, pal_y_scale, down_interpol, up_interpol):
    """Simulates PAL encoding on an image. To do this it uses the source
    image to make two new images: a high resolution "luminance" image and a
    low resolution "chrominance" image. Then it combines these two images to
    give you the finished result.

    The method used by this plug-in is explained in more detail on my blog:
    http://kecskebak.blogspot.com/2009/09/tapeheads-revisited.html

    There is a choice of PAL encoding systems.

    PAL-D averages out the colour of adjacent lines, so to simulate this I
    simply halve the vertical resolution when creating the luminance and
    chrominance images."""

    gimp.context_push()
    img.undo_group_start()

    # Work out image scaling
    width = layer.width
    height = layer.height

    chrominance_width = width / 3
    chrominance_height = height * pal_y_scale
    luminance_width = width - chrominance_width
    luminance_height = height * pal_y_scale

    # Luminance layer
    luminance_layer = layer

    # Create a chrominance layer
    chrominance_layer = layer.copy(1)
    img.add_layer(chrominance_layer)
    pdb.gimp_layer_set_mode(chrominance_layer, ADDITION_MODE)

    # Apply levels to luminance layer
    adjust_levels(luminance_layer, 76, 150, 29)

    # Apply levels to chrominance layer
    adjust_levels(chrominance_layer, 179, 105, 226)

    # Scale luminance layer
    scale(luminance_layer, luminance_width, luminance_height,
          down_interpol) 
    scale(luminance_layer, width, height, up_interpol)

    # Scale chrominance layer
    scale(chrominance_layer, chrominance_width, chrominance_height,
          down_interpol) 
    scale(chrominance_layer, width, height, up_interpol)

    # Merge chrominance and luminance layers
    layer = pdb.gimp_image_merge_down(img, chrominance_layer, CLIP_TO_IMAGE)

    img.undo_group_end()
    gimp.context_pop()

def scale(layer, new_width, new_height, interpolation):
    local_origin = False    
    pdb.gimp_layer_scale_full(layer, new_width, new_height, local_origin,
                              interpolation)

def adjust_levels(layer, r, g, b):
    low_input = 0
    high_input = 255
    gamma = 1.0
    low_output = 0

    pdb.gimp_levels(layer , HISTOGRAM_RED, low_input, high_input,
                    gamma, low_output, r)
    pdb.gimp_levels(layer , HISTOGRAM_GREEN, low_input, high_input,
                    gamma, low_output, g)
    pdb.gimp_levels(layer , HISTOGRAM_BLUE, low_input, high_input,
                    gamma, low_output, b)

register(
    "python-fu-palhd",
    N_("Makes image look PAL encoded."),
    "Makes image look PAL encoded.",
    "Dave Jeffery",
    "Dave Jeffery",
    "2009",
    N_("PAL _HD..."),
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image", _("Input image"), None),
        (PF_DRAWABLE, "drawable", _("Input drawable"), None),
        (PF_RADIO, "pal_y_scale", _("PAL version"), 1.0,
         ((_("PAL-S (Simple PAL)"), PAL_S),
          (_("PAL-D"), PAL_D))),
        (PF_RADIO, "down_interpol", _("Down-scaling interpolation method"), 2,
         ((_("None"), INTERPOLATION_NONE),
          (_("Linear"), INTERPOLATION_LINEAR),
          (_("Cubic"), INTERPOLATION_CUBIC),
          (_("Sinc Lanczos"), INTERPOLATION_LANCZOS))),
        (PF_RADIO, "up_interpol", _("Up-scaling interpolation method"), 3,
         ((_("None"), INTERPOLATION_NONE),
          (_("Linear"), INTERPOLATION_LINEAR),
          (_("Cubic"), INTERPOLATION_CUBIC),
          (_("Sinc Lanczos"), INTERPOLATION_LANCZOS)))        
    ],
    [],
    palhd,
    menu="<Image>/Filters/Artistic",
    domain=("gimp20-python", gimp.locale_directory)
    )

main()
