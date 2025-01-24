""" analyze_videofile.py

This script applies the detector to a videostream generated from a video file.
The results are dispalyed with bounding boxes, labels and scores.
You can use the keyboard keys <esc>, <return> or <q> to cancel the presentation.

The script requires the class detector.py

SLW Jan-2025
"""

import os
import cv2
import detector
import time
import sys

# Directories
video_file = "<my_video_file.mp4>"
project_dir = "<my_project>"
video_dir = "<my_video_folder>"
model_dir = "model"

# Print instructions
print("Analyze video stream")
print(30 * "=")
print()

# Paths 
video_path = os.path.join(project_dir, video_dir)
if not os.path.isdir(video_path):
    print("Error: can't find video path: '" + video_path + "' !")
    sys.exit(1)
model_path = os.path.join(project_dir, model_dir)
if not os.path.isdir(model_path):
    print("Error: can't find model path: '" + model_path + "' !")
    sys.exit(1)

# Constants
threshold = 0.75  #  Detector threshold
delay = 0.025     # delay time between displayed frames

# Detector
print("Starting detector ...")
dtc = detector.Detector(model_path)

# Opening video stream
print("Opening video file ...")
# cam = cv2.VideoCapture(1)
video_stream = cv2.VideoCapture(os.path.join(project_dir, video_dir, video_file))
if (video_stream.isOpened() == False):
    print("Error: could not open the video file:", video_file)
    sys.exit(1)

print("Using video file:", video_file)
frame_ps = int(video_stream.get(5))
print("Frame rate:", frame_ps, "frames per sec")
frame_cnt = video_stream.get(7)
print("Frame count:", frame_cnt)
print("Frame size:", int(video_stream.get(3)), '*', int(video_stream.get(4)))
print()

error_cnt = 0
running = True
print("Press <return> or <esc> for exit.")

while running:
    # get image from the video stream
    success, img = video_stream.read()
    if not success:
        # if not successful, handle error
        print("Failed to grab frame!")
        error_cnt += 1
        if error_cnt > 10:
            print("Too many errors ... exiting program!")
            running = False
    
    else:
        error_cnt = 0
        # detect objects
        boxes, classes, scores = dtc.detect_objects(img)
        # add boxes to the image
        for idx in range(10):
            if scores[idx] >= threshold:
               img = dtc.add_box(img, boxes[idx],
                                 dtc.labels[classes[idx]] + ": " + str(round(scores[idx]*100)) + '%')
            else:
                break
        # show the image and get key from keyboard
        cv2.imshow(project_dir, img)
        key = cv2.waitKey(1) & 0xff
        # process key
        if key in (13, 27, 113): # codes for <return>, <esc>, <q>
            running = False
            
    time.sleep(delay)

# Done!
print()
print("Closing video stream")
video_stream.release()
cv2.destroyAllWindows()
