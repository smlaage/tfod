""" check_images.py

This scripts checks labeled images in preparation 
for the use in tensor flow training. It checks the following topics:
  - For each image file (*.jpg, *.jpeg or *.png) there needs to be exactly one label file (*.xml)
  - The size of the images
  - The labels 
In case everything is okay, the shows basic statistics:
  - the count of different image shapes
  - the number of images per label
  - a Python label-statement as needed to create the labels for training
The script creates a zip file including all images and labels.

SLW Oct-2024
"""

import sys
import os
import cv2
import pandas as pd
import shutil

# Set files and paths
project_dir = "microorganismn"
image_dir = "images"
zip_file = "microorganismn_images"
image_path = os.path.join(project_dir, image_dir)
file_lst = os.listdir(image_path)

print()
print("Checking images in " + str(image_path) + " ...")
files = {}
error_cnt = 0

for index, f in enumerate(file_lst, 1):
    print(index, end='\r')
    pos = f.rfind('.')
    if pos > 0 and pos < len(f) - 2:
        error = False
        ending = f[pos+1:]
        name = f[:pos]
        if name not in files:
            files[name] = (False, False, "", False, None)
        if ending.casefold() in ("png", "jpg", "jpeg"):
            img = cv2.imread(os.path.join(image_path, f))
            width, height, channels = img.shape
            files[name] = (True, files[name][1], files[name][2], img.shape)
        elif ending.casefold() == "xml":
            files[name] = (files[name][0], True, files[name][2], files[name][3])
            xml = open(os.path.join(image_path, f), "r")
            s = xml.read()
            xml.close()
            pos1 = s.find("<object>")
            if pos1 < 10:
                print("Error in " + f + " - can't find tag '<object>'!")
                error = True
            if not error:
                pos2 = s[pos1:].find("<name>")
                if pos2 < 5:
                    print("Error in " + f + " - can't find tag '<name>'!")
                    error = True
            if not error:
                pos3 = s[pos1 + pos2:].find("</name>")
                if pos3 < 5:
                    print("Error in " + f + " - can't find tag '</name>'!")
                    error = True
            if not error:
                label = s[pos1 + pos2 + 6 : pos1 + pos2 + pos3]
                files[name] = (files[name][0], files[name][1], label, files[name][3])
            else:
                error_cnt += 1
        else:
            print("Error in " + f + " - filetype not recognized!")
            error_cnt += 1
                  
# Show error status
if error_cnt > 0:
    print(error_cnt, "error(s) detected")
    sys.exit(1)

# Convert to dataframe
files = pd.DataFrame.from_dict(files, orient='index', columns = ['jpg', 'xml', 'label', 'shape'])

# Check for missing jpg files
jpg_missing = len(files[files['jpg'] == False])
if jpg_missing > 0:
    print("Missing jpg files:", jpg_missing)
    print(files[files['jpg'] == False])
    error = True
    print()

# Check for missing xml files
xml_missing = len(files[files['xml'] == False])
if xml_missing > 0:
    print("Missing xml files:", xml_missing)
    print(files[files['xml'] == False])
    error = True
    print()

if error:
    sys.exit(1)

print(40 * "=")
print("Image check okay!")
print()

print("Image shapes:")
shapes = files['shape'].value_counts()
shape_len = 0
for idx, cnt in shapes.items():
    if len(str(idx)) > shape_len:
        shape_len = len(str(idx))
for idx, cnt in shapes.items():
    format_str = "- {:" + str(shape_len + 1) + "s}:{:4d}"
    print(format_str.format(str(idx), cnt))
print()

print("Labels:")
labels = files['label'].value_counts()
label_len = labels.index.str.len().max()
for idx, cnt in labels.items():
    format_str = "- {:" + str(label_len + 1) + "s}:{:4d}"
    print(format_str.format(idx, cnt))
print()

print("Label statement:")
s = "label = ['"
for l in labels.index:
    s += str(l) + "', '"
s = s[:-3] + ']'
print(s)
print()

print("Creating zip file:", os.path.join(project_dir, zip_file) + ".zip")
shutil.make_archive(os.path.join(project_dir, zip_file), 'zip', image_path)
print("Done!")
print()
