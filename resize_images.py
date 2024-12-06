"""
resize_image.py

The script reduces the size of all images in folder <original> to 1024x768 pixel.
It stores the resized images in the target folder <images>.
The target filename is getting a trailing "_reduced" to its name.
(e.g. "abc02.jpg" becomes "abc02_reduced.jpg"). The trailer can be changed as needed.

The folder names need to be adjusted according to your needs.

Dependencies: OpenCV

SLW - 08-2023
"""

import os
import cv2

# Directories
project_dir = "things"
source_image_dir = "originals"
source_image_path = os.path.join(project_dir, source_image_dir)
dest_image_dir = "images"
dest_image_path = os.path.join(project_dir, dest_image_dir)

trailer = "_reduced"

print("Resizing images from folder '" + source_image_path + "' to '" + dest_image_path + "'") 

# Read source data
file_list = os.listdir(source_image_path)
cnt = 0
if len(file_list) == 0:
    print("The source folder is empty!!!")
else:
    # Resize images one by one
    for file in file_list:
        pos = file.rfind('.')
        if pos <= 0:
            continue
        name = file[:pos]
        ending = file[pos+1:]
        if ending in ("jpg", "png"):
            print(cnt, end='\r')
            img = cv2.imread(os.path.join(source_image_path, file))
            height, width = img.shape[:2]
            if width > 1024:
                img = cv2.resize(img, (1024, height * 1024 // width))
            elif height > 1024:
                img = cv2.resize(img, (width * 1024 // height), 1024)
            cv2.imwrite(os.path.join(dest_image_path, name + trailer + '.' + ending), img)
            print(file, "processed", end='\r')
            cnt += 1
        
print(50 * ' ', end='\r')
print(cnt, "images processed")
print("Done")
