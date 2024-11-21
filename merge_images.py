#!/usr/bin/python3
#
# This script is designed to merge (either horizontally
# or vertically a set of images. In this specific case
# the script will merge salinity and lx plots.
#


######################################################
#
# requirements
#
######################################################

from PIL import Image
import sys
import os


######################################################
#
# input params
# - the folder containing the images to be merged
# - 0 or 1 to choose between horiz. or vertical merge
# - the image to overlay
#
######################################################

# Directory where your images are located
image_dir = sys.argv[1]
vertical = int(sys.argv[2]) # 0 = horizontal, 1 = vertical
overlay = sys.argv[3] 

######################################################
#
# process images
#
######################################################

# iterate over the dates to 
for d in range(0, 366):

    # build filenames
    salinity_plot = os.path.join(image_dir, f"salinity_plot_{d:04d}.png")
    lx_plot = os.path.join(image_dir, f"lx_plot_{d:04d}.png")

    # check if files exist, otherwise skip to next iteration
    if not os.path.exists(salinity_plot):
        continue
    if not os.path.exists(lx_plot):
        continue
    
    # salinity
    salinity_img = Image.open(salinity_plot).convert("RGBA")
    salinity_width, salinity_height = salinity_img.size
    
    # lx
    lx_img = Image.open(lx_plot).convert("RGBA")
    lx_width, lx_height = lx_img.size

    if vertical:

        # Calculate the total width and height for the combined image
        total_width = max(salinity_width, lx_width)
        total_height = salinity_height + lx_height
    
        # Create a new blank image with the calculated size
        combined_img = Image.new('RGB', (total_width, total_height), color='white')
    
        # Paste the salinity image on the left
        combined_img.paste(salinity_img, (0, 0))
    
        # Paste the lx image on the right
        # combined_img.paste(lx_img_res, (salinity_width, 0))
        combined_img.paste(lx_img, (0, salinity_height))
    
        # overlay the logo        
        logo_img = Image.open(overlay).convert("RGBA")
        combined_img.paste(logo_img, (0,0), logo_img)

        # Save the combined image with a new filename
        print(f'Saving VERT_combined_plot_{d:04d}.png')
        combined_img.save(os.path.join(image_dir, f'VERT_combined_plot_{d:04d}.png'))

    else:
        
        # Calculate the total width and height for the combined image
        total_width = salinity_width + lx_width
        total_height = max(salinity_height, lx_height)
    
        # Create a new blank image with the calculated size
        combined_img = Image.new('RGB', (total_width, total_height), color='white')
    
        # Paste the salinity image on the left
        combined_img.paste(salinity_img, (0, 0))
    
        # Paste the lx image on the right
        combined_img.paste(lx_img, (salinity_width, 0))

        # overlay the logo
        logo_img = Image.open(overlay).convert("RGBA")
        combined_img.paste(logo_img, (0,0), logo_img)
    
        # Save the combined image with a new filename
        print(f'Saving HORIZ_combined_plot_{d:04d}.png')
        combined_img.save(os.path.join(image_dir, f'HORIZ_combined_plot_{d:04d}.png'))

    break
        
    # Close the images to free up resources
    salinity_img.close()
    lx_img.close()
