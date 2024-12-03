"""
resize_image.py

The script reduces the size of all images in folder <original> to 1024x768 pixel.
It stores the resized images in the target folder <images>.

The folder names need to be adjusted according to your needs.

Dependencies: OpenCV

SLW - 08-2023
"""

import os
import cv2

# Directories
project_dir = "."
source_image_dir = "original"
source_image_path = os.path.join(project_dir, source_image_dir)
dest_image_dir = "images"
dest_image_path = os.path.join(project_dir, dest_image_dir)

print("Resizing images from folder '" + source_image_path + "' to folder '" + dest_image_path + "'") 

# Read source data
file_list = os.listdir(source_image_path)
cnt = 0

# Resize images one by one
for file in file_list:
    if file[-4:] in (".jpg", ".png"):
        print(cnt, end='\r')
        img = cv2.imread(os.path.join(source_image_path, file))
        height, width = img.shape[:2]
        if width > 1024:
            img = cv2.resize(img, (1024, height * 1024 // width))
        elif height > 1024:
            img = cv2.resize(img, (width * 1024 // height), 1024)
        cv2.imwrite(os.path.join(dest_image_path, file), img)
        print(file, "processed", end='\r')
        cnt += 1
    
print(cnt, "images processed")
print("Done")

