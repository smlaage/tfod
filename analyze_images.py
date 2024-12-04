""" analyze_images.py

SLW Oct-2024
"""

import os
import cv2
import detector

threshold = 0.3

def show_box(frame, box, label, score):
    height, width = img.shape[:2]
    ymin = int(max(1,(box[0] * height)))
    xmin = int(max(1,(box[1] * width)))
    ymax = int(min(image_height,(box[2] * height)))
    xmax = int(min(image_width,(box[3] * width)))  
    cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
    label_str = "{:s}: {:d}%".format(label, int(score * 100))
    label_size, base_line = cv2.getTextSize(label_str, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
    label_ymin = max(ymin, label_size[1] + 10) # Make sure not to draw label too close to top of window
    cv2.rectangle(frame, (xmin, label_ymin-label_size[1]-10), (xmin+label_size[0], label_ymin+base_line-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
    cv2.putText(frame, label_str, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
    return frame

#===========================================================================================================

# Instructions
print("Analyze images ...")
print("- Press 's' to move to the previous and 'd' to move to the next image.")
print("- Press 'a' to move 10 images backwards and 'f' to move 10 images forward.")
print("- Press <esc> to exit.")
print()

# Directories
project_dir = "sign-language"
image_dir = "images"
image_path = os.path.join(project_dir, image_dir)
model_dir = "model"
model_path = os.path.join(project_dir, model_dir)

# Constants
threshold = 0.4
image_height, image_width = 768, 1024
image_step = 10

# Detector
print("Starting detector ...")
dct = detector.Detector(model_path)

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
    boxes, classes, scores = dct.detect_objects(img)
    #cv2.imshow("", img)
    for i in range(10):
        if scores[i] > threshold:
            print("   - Class:", dct.labels[classes[i]], 
                  "  Score:", round(scores[i] * 100), "%")
            img = show_box(img, boxes[i], dct.labels[classes[i]], scores[i])
        else:
            break
    # Show the image and wait for the keyboard
    cv2.imshow("", img)
    key = cv2.waitKey(0)
    # Analyze keys pressed 
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
