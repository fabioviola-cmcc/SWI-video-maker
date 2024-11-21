#!/usr/bin/python3
#
# This script creates a video starting from the
# images produced by merge_images.py script.
# Input parameters are:
# - input directory
# - orientation (0 = horiz, 1 = vert)
# - frame per second
#

##################################################
#
# requirements
#
##################################################

import cv2
import sys
import os


##################################################
#
# input params
#
##################################################

# Directory where your merged images are located
image_dir = sys.argv[1]
orientation = sys.argv[2]
fps = int(sys.argv[3])


##################################################
#
# input params
#
##################################################

# Define the codec and create a VideoWriter object
if orientation:
    outfile = os.path.join(image_dir, f"VERT_output_video.mp4")
    image_files = sorted([f for f in os.listdir(image_dir) if f.startswith('VERT_combined_plot_') and f.endswith('.png')])    
else:
    outfile = os.path.join(image_dir, f"HORIZ_output_video.mp4")
    image_files = sorted([f for f in os.listdir(image_dir) if f.startswith('HORIZ_combined_plot_') and f.endswith('.png')])    

# Read the first image to get dimensions
first_image_path = os.path.join(image_dir, image_files[0])
frame = cv2.imread(first_image_path)
height, width, layers = frame.shape
    
# initialise the video    
video = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
        
# Iterate through the image files and write them to the video
for image_file in image_files:
    img_path = os.path.join(image_dir, image_file)
    img = cv2.imread(img_path)
    video.write(img)

# Release the VideoWriter
video.release()

print(f"Video {outfile} created successfully.")
