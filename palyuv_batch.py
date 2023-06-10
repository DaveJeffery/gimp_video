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

import os
import random

from gimpfu import *

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)

def palyuv_batch(img, layer, y_blur_x, y_blur_y, 
                 cb_blur_x, cb_blur_y, cr_blur_x, cr_blur_y, 
                 oilyfy, input_folder, output_folder):
    ''' Apply the PALYUV and Oilfy filters to PNG or JPEG images in a folder.
    
    Parameters:
    img : image The current image (unused).
    layer : layer The layer of the image that is selected (unused).
    input_folder : string The folder of the images that must be modified.
    output_folder : string The folder in which save the modified images.
    '''
    
    # Iterate the folder
    for file in os.listdir(input_folder):
        try:
            # Build the full file paths.
            input_path = os.path.join(input_folder, file)
            output_path = os.path.join(output_folder, file)
        
            # Open the file if is a JPEG or PNG image.
            image = None
            if(file.lower().endswith(('.png'))):
                image = pdb.file_png_load(input_path, input_path)
            if(file.lower().endswith(('.jpeg', '.jpg'))):
                image = pdb.file_jpeg_load(input_path, input_path)
                
            # Do nothing if the file is not an image.
            if(image == None):
                continue
            
            # Do nothing if the image contains no layers.
            if(len(image.layers) < 1):
                continue
                
            layer = image.layers[0]
            
            #TODO Add Oilify here
            if oilyfy:
                random.seed()
                mask_size = random.randrange(5, 8, 1)
                pdb.plug_in_oilify_enhanced(image, layer, 1, mask_size, None, 8, None)
            
            pdb.python_fu_palyuv(image, layer, y_blur_x, y_blur_y, 
                                 cb_blur_x, cb_blur_y, cr_blur_x , cr_blur_x)
            
            # Save the image.
            if(file.lower().endswith(('.png'))):
                pdb.file_png_save(image, image.layers[0], output_path, 
                                  output_path, 0, 9, 0, 0, 0, 0, 0)
            if(file.lower().endswith(('.jpeg', '.jpg'))):
                pdb.file_jpeg_save(image, layer, output_path, 
                                   output_path, 0.9, 0, 0, 0, 
                                   "Created with GIMP", 0, 0, 0, 0)
                
        except Exception as err:
            gimp.message("Unexpected error: " + str(err))


register(
    "python-fu-palyuv-batch",
    N_("Makes image look PAL encoded using YUV decomposition."),
    "Makes image look PAL encoded using YUV decomposition.",
    "Dave Jeffery",
    "Dave Jeffery",
    "2013",
    N_("PAL Y_UV batch..."),
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image", _("Input image"), None),
        (PF_DRAWABLE, "drawable", _("Input drawable"), None),
        (PF_SLIDER, "y_blur_x", _("Y blur X"), 4, (0, 100, 1)),
        (PF_SLIDER, "y_blur_y", _("Y blur Y"), 2, (0, 100, 1)),
        (PF_SLIDER, "cb_blur_x", _("U blur X"), 32, (0, 100, 1)),
        (PF_SLIDER, "cb_blur_y", _("U blur Y"), 16, (0, 100, 1)),
        (PF_SLIDER, "cr_blur_x", _("V blur X"), 32, (0, 100, 1)),
        (PF_SLIDER, "cr_blur_y", _("V blur Y"), 16, (0, 100, 1)),        
        (PF_TOGGLE, "oilyfy", _("Oilify?"), False),
        (PF_DIRNAME, "input_folder", _("Input directory"), os.getcwd()),
        (PF_DIRNAME, "output_folder", _("Output directory"), os.getcwd())           
    ],
    [],
    palyuv_batch,
    menu="<Image>/Filters/Artistic",
    domain=("gimp20-python", gimp.locale_directory)
    )

main()