This is a loose collection if Python scripts that are helpful for tensorflow image detection.
SLW - Oct 2024

check_images.py: This scripts checks labeled images in preparation 
for the use in tensor flow training. It checks the following topics:
  - For each image file (*.jpg, *.jpeg or *.png) there needs to be exactly one label file (*.xml)
  - The size of the images
  - The labels 
In case everything is okay, the shows basic statistics:
  - the count of different image shapes
  - the number of images per label
  - a Python label-statement as needed to create the labels for training
The script creates a zip file including all images and labels.
