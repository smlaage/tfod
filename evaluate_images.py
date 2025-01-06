""" evaluate_images.py

This scripts evaluates the prediction for a single image. It compares the true objects (as
specified by the annotations) to the estimated objects (as found by the object detector).

Prerequisites:
- a trained tensorflow-lite object detector (tflite.detect and labelmap.txt)
- an image file (filetype .png or .jpg)
- an annotation (label) file (filetype .xml)
Image and label files must have the same name (but different endings, obviously)

Output:
(1) list of true objects:
    - running index of true object (starting at 0)
    - label of the true object
    - running index of estimated object (starting at 0)
    - label of the estimated object
    - score of the estimated object
    - factor or the overlap area (intersection)
    - match found, overlap > 50% (True or False)
(2) list of estimated objects:
    - running index of the estimated object (starting at 0)
    - label of the estimated object
    - score of the estimated object
    - match found (True or False)
    
The visualisation shows the true and estimated objects with coloured rectangles.
- green = true object with matching estimated object
- yellow = true object without matching estimated object
- blue = estimated object with matching true object
- red = estimated object without matching true object

SLW Dec-2024
"""

import os
import evaluator


# Directories
project_dir = "micro-organisms"
image_dir = "images"
model_dir = "model"

# Print instructions
print("Evaluate images ...")
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

# Start evaluator
evl = evaluator.Evaluator(model_path)

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
    
    pos = f.rfind('.')
    if pos > 0:
        f = f[:pos]
    else:
        print("Error: could not fin filetype:", f)
        continue
    
    if f[pos+1 :].casefold() == "xml".casefold():
        continue
    
    print(str(pnt+1) + ": " + f)
    # Evaluate image
    true_lst, est_lst, key = evl.evaluate_img(f, image_path, verbose=False, show_img=True)
    print("True Objects:")
    print("Idx  True Label           Est. Label           Correct  Score Localization")
    for true_obj in true_lst:
        print("{:3d}  {:20s} {:20s} {:6s}  {:5.1f}%       {:5.1f}%".format(
              true_obj[0] + 1, true_obj[1], true_obj[3], "Yes" if true_obj[1] == true_obj[3] else "No",
              true_obj[4]*100, true_obj[5]*100))
    print("Estimated Objects:")
    print("Idx Est. Label             Score  Match")
    for est_obj in est_lst:
        print("{:3d} {:20s}  {:5.1f}%  {:5s}".format(
              est_obj[0] + 1, est_obj[1], est_obj[2]*100, "True" if est_obj[3] else "False"))
    print()    

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

# Cleanup
evl.cleanup()
print("Done!")
