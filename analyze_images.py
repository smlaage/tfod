""" analyze_images.py

This script walks through a folder of images, runs the detector and displays the results including boxes.
You can use the keyboard to move forwards of backwards, frame by frame or in larger steps.

SLW Oct-2024
"""

import os
import cv2
import detector

# Directories
project_dir = "micro-organisms"
image_dir = "images"
model_dir = "model"

# Print instructions
print("Analyze images ...")
print("- Press 's' to move to the previous and 'd' to move to the next image.")
print("- Press 'a' to move 10 images backwards and 'f' to move 10 images forward.")
print("- Press <esc> to exit.")
print()

# Paths 
image_path = os.path.join(project_dir, image_dir)
model_path = os.path.join(project_dir, model_dir)

# Constants
threshold = 0.5
image_height, image_width = 768, 1024
image_step = 10

# Detector
print("Starting detector ...")
dtc = detector.Detector(model_path)

# Image directory
print("Reading image directory ...")
files = os.listdir(image_path)
image_files = [f for f in files if f[-4:] in ('.jpg', '.png')]
files_cnt = len(image_files)
pnt = 0
print(files_cnt, "images found")
print()

while True:
    # Read image
    f = image_files[pnt]
    print(str(pnt + 1) + ": " + f)
    img = cv2.imread(os.path.join(image_path, f))
    height, width = img.shape[:2]
    if width > image_width:
        img = cv2.resize(img, (image_width, height * image_width // width))
        print("   - image resized")
        height, width = img.shape[:2]
    if height > image_height:
        img = cv2.resize(img, (width * image_height // height, image_height))
        print("   - image resized")
    # Find objects
    boxes, classes, scores = dtc.detect_objects(img)
    # Add boxes
    for i in range(10):
        if scores[i] > threshold:
            img = dtc.add_box(img, boxes[i],
                              dtc.labels[classes[i]] + ": " + str(round(scores[i]*100)) + '%')
        else:
            break
    # Show the image and wait for a key pressed
    cv2.imshow("", img)
    key = cv2.waitKey(0) & 0xff
    
    # Analyze keys pressed and move to the next image(s)
    if chr(key) in ('a', 'A'):
        pnt -= image_step;
        if pnt < 0:
            pnt = files_cnt + pnt
    elif chr(key) in ('s', 'S'):
        pnt -= 1;
        if pnt < 0:
            pnt = files_cnt + pnt
    elif chr(key) in ('d', 'D'):
        pnt += 1
        if pnt >= files_cnt:
            pnt = files_cnt - 1
    elif chr(key) in ('f', 'F'):
        pnt += image_step
        if pnt >= files_cnt:
            pnt = files_cnt - 1
    elif key == 27:
        break
    else:
        pnt += 1
        if pnt >= files_cnt:
            break

# Clean up
cv2.destroyAllWindows()
print("Done!")
