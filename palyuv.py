#!/usr/bin/env python

#   The GIMP PALYUV plugin - PAL effect plugin for The GIMP.
#   Copyright (C) 2009, 2013  Dave Jeffery <david.richard.jeffery@gmail.com>
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

import random

from gimpfu import *

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)

def palyuv(img, layer, y_blur_x, y_blur_y, 
           cb_blur_x, cb_blur_y, cr_blur_x, cr_blur_y):
    """Simulates PAL encoding on an image."""

    y_blur = (y_blur_x, y_blur_y)
    cb_blur = (cb_blur_x, cb_blur_y)
    cr_blur = (cr_blur_x, cr_blur_y)

    gimp.context_push()
    img.undo_group_start()

    # Decompose into YUV
    yuv_img, none1, none2, none3 = pdb.plug_in_decompose(img, 
                                                         layer, 
                                                         "YCbCr_ITU_R470", 
                                                         1)

    # Blur Y layer
    layer_Y = yuv_img.layers[0]
    pdb.plug_in_gauss_rle2(yuv_img, layer_Y, y_blur[0], y_blur[1])

    # Blur U layer
    layer_Cb = yuv_img.layers[1]
    pdb.plug_in_gauss_rle2(yuv_img, layer_Cb, cb_blur[0], cb_blur[1])

    # Blur V layer
    layer_Cr = yuv_img.layers[2]
    pdb.plug_in_gauss_rle2(yuv_img, layer_Cr, cr_blur[0], cr_blur[1])
 
    # Recompose into RGB 
    yuv_img = pdb.plug_in_drawable_compose(yuv_img, layer_Y, layer_Cb, layer_Cr, None, "YCbCr_ITU_R470")


    tmp = pdb.gimp_layer_new_from_visible(yuv_img, img, "PALYUV")
    pdb.gimp_image_insert_layer(img, tmp, None, -1)
    
    layer = pdb.gimp_image_merge_down(img, tmp, CLIP_TO_IMAGE)
    
    img.undo_group_end()
    gimp.context_pop()

register(
    "python-fu-palyuv",
    N_("Makes image look PAL encoded using YUV decomposition."),
    "Makes image look PAL encoded using YUV decomposition.",
    "Dave Jeffery",
    "Dave Jeffery",
    "2013",
    N_("PAL _YUV..."),
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image", _("Input image"), None),
        (PF_DRAWABLE, "drawable", _("Input drawable"), None),
        (PF_SLIDER, "y_blur_x", _("Y blur X"), 4, (0, 100, 1)),
        (PF_SLIDER, "y_blur_y", _("Y blur Y"), 2, (0, 100, 1)),
        (PF_SLIDER, "cb_blur_x", _("U blur X"), 32, (0, 100, 1)),
        (PF_SLIDER, "cb_blur_y", _("U blur Y"), 16, (0, 100, 1)),
        (PF_SLIDER, "cr_blur_x", _("V blur X"), 32, (0, 100, 1)),
        (PF_SLIDER, "cr_blur_y", _("V blur Y"), 16, (0, 100, 1))
    ],
    [],
    palyuv,
    menu="<Image>/Filters/Artistic",
    domain=("gimp20-python", gimp.locale_directory)
    )

main()
