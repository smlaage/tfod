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

# Set files and paths
project_dir = "micro-organisms"
image_dir = "images"
model_dir = "model"
image_name = "paramecium_caudatum_Snap-592"

# Directories
image_path = os.path.join(project_dir, image_dir)
model_path = os.path.join(project_dir, model_dir)

# Start evaluator
evl = evaluator.Evaluator(model_path)

# Evaluate image
true_lst, est_lst, _ = evl.evaluate_img(image_name, image_path, verbose=False, show_img=True)

# Show results
print("True objects:")
for true_obj in true_lst:
    print(true_obj)
print("Estimated objects:")
for est_obj in est_lst:
    print(est_obj)

# Cleanup
evl.cleanup()
print("Done!")
