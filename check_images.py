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

def replace_blanks(image_path):
    """ replace blanks """
    files = os.listdir(image_path)
    cnt = 0
    for f in files:
        if f.count(' ') > 0:
            f_new = f.replace(' ', '_')
            print("File " + f + ": removing blanks")
            os.rename(os.path.join(image_path, f), os.path.join(image_path, f_new))
            cnt += 1
    return cnt


def analyze_xml(files):
    """ analyze XML file for consistency of file names """
    cnt = 0
    for idx, row in files.iterrows():
        with open(os.path.join(image_path, idx + '.xml'), "r") as xml:
            s = xml.read()
        # Compare filename in xml to actual filename       
        start_pos = s.find("<filename>") + 10
        end_pos = s[start_pos:].find("</filename>")
        xml_name = s[start_pos : start_pos + end_pos]
        target_name = idx + '.' + row['image']
        if xml_name != target_name:
            print("Correcting XML file for " + target_name)
            new_s = s[:start_pos] + target_name + s[start_pos + end_pos:]
            with open(os.path.join(image_path, idx + '.xml'), "w") as xml:
                xml.write(new_s)
            cnt += 1
    return cnt

#= main program starts here ===================================================

# Set files and paths
project_dir = "sign-language"
image_dir = "images"
zip_file = "sign-language_images"
image_path = os.path.join(project_dir, image_dir)
file_lst = os.listdir(image_path)

# Print title
print()
title = "Checking images in " + str(image_path) + " ..."
print(title)
print(len(title) * "=")
print()

# Replacing blanks in filenames
print("Checking for blanks in filenames ...")
cnt = replace_blanks(image_path)
if cnt > 0:
    print(cnt, "filename(s) corrected!")
    print()
print("Done")
print()

# Create list of files
files = {}
error_cnt = 0
error = False

# Walk thorugh the list fo files
for index, f in enumerate(file_lst, 1):
    print(index, end='\r')
    pos = f.rfind('.')
    if pos > 0 and pos < len(f) - 2:
        error = False
        ending = f[pos+1:]
        name = f[:pos]
        if name not in files:
            files[name] = ("", False, "", False, None)
        if ending.casefold() in ("jpg", "png"):
            img = cv2.imread(os.path.join(image_path, f))
            width, height, channels = img.shape
            files[name] = (ending, files[name][1], files[name][2], img.shape)
        elif ending.casefold() == "xml":
            files[name] = (files[name][0], True, files[name][2], files[name][3])
            # Read xml file
            xml = open(os.path.join(image_path, f), "r")
            s = xml.read()
            xml.close()
            # Find label
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
    # sys.exit(1)

# Convert to dataframe
files = pd.DataFrame.from_dict(files, orient='index', columns = ['image', 'xml', 'label', 'shape'])

# Check for missing jpg files
images_missing = len(files[files['image'] == ""])
if images_missing > 0:
    print("Missing image files:", images_missing)
    print(files[files['image'] == ""])
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
    print("Error!")
else:
    print(len(title) * "-")
    print("Image check okay!")
    print()
    
    # Check consistency of filenames in XML files
    print("Checking consistency of filenames in XML files ...")
    cnt = analyze_xml(files)
    if cnt > 0:
        print(cnt, "XML files corrected!")
        print()
    print("Done")
    print()

    print("Results:")
    print(len(title) * "-")
    print("Image shapes (height, width, layers):")
    shapes = files['shape'].value_counts()
    shape_len = 0
    for idx, cnt in shapes.items():
        if len(str(idx)) > shape_len:
            shape_len = len(str(idx))
    for idx, cnt in shapes.items():
        format_str = "- {:" + str(shape_len + 1) + "s}:{:4d}"
        print(format_str.format(str(idx), cnt))

    print("Labels and frequency:")
    labels = files['label'].value_counts()
    label_len = labels.index.str.len().max()
    for idx, cnt in labels.items():
        format_str = "- {:" + str((label_len) + 2) + "s} :{:4d}"
        print(format_str.format("'" + idx +"'", cnt))

    print("Python label statement:")
    s = "- labels = ['"
    for l in labels.index:
        s += str(l) + "', '"
    s = s[:-3] + ']'
    print(s)
    print()

    response = input("Do you want to create a zip file? (Y/N)")
    if response.strip()[0] in ('y', 'Y'):
      print("Creating zip file:", os.path.join(project_dir, zip_file) + ".zip")
      shutil.make_archive(os.path.join(project_dir, zip_file), 'zip', image_path)
      print("Done!")
    print()
  
