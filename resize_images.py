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

img_dir = "images"
org_dir = "original"
file_list = os.listdir(org_dir)
cnt = 0

print("Resizing images from folder '" + org_dir + "' to '" + img_dir + "'") 

for file in file_list:
    if file[-4:] in (".jpg", ".png"):
        print(cnt, end='\r')
        img = cv2.imread(os.path.join(org_dir, file))
        height, width = img.shape[:2]
        if width > 1024:
            img = cv2.resize(img, (1024, height * 1024 // width))
        cv2.imwrite(os.path.join(img_dir, file), img)
        print(file, "processed", end='\r')
        cnt += 1
    
print(cnt, "images processed")
print("Done")
