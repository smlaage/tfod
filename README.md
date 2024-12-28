<h2><b>Overview</b></h2> 
<p>This is a loose collection of helpful Python scripts to support tensorflow object detection.
  It includes the following scripts:</p>
<ul style="list-style-type:square;">
  <li>check_images.py - prepares and checks image and label files prior to the model training</li>
  <li>resize_images.py - resizes images to the prefered size (e.g.1024x768) prior to model training</li>
  <li>prefix_files.py - renames all files in an image with a given prefix (usually the name of the class of an image)</li>
  <li>analyze_images.py - runs the tflite detector on all images in a given directory and shows the objects found</li>
  <li>detector.py - this is a python class providing easy access to the tensorflow lite detector</li>
  <li>evaluator.py - this is a python class to evaluate the performance of a TensorFlow object detection algorithm.</li>
</ul>
<p>The recommended folder structure is shown in "folder_structrue.png".</p>
<p>Dependencies:</p>
<ul style="list-style-type:square;">
  <li>Running under Windows: tensorflow.lite (this is incldued in the full tensorflow package)</li>
  <li>Or running on a Raspberry Pi: tflite_runtime.interpreter</li>
  <li>cv2 (OpenCV)</li>
  <li>pandas</li>
  <li>numpy</li>
  <li>shutil</li>
  <li>sys</li>
  <li>os</li>
</ul>
<p>SLW - Oct 2024</p>

<h2><b>check_images.py</b></h2> 
<p>This scripts checks labeled images in preparation for tensorflow training. 
  All images and label-files must be in a single folder. Ususally the images folder is a subfolder to the project folder.
The path to project and image folders must be provided inside the script (line 24 and 25).</p> 
<p>The script checks the following topics:</p>
<ul style="list-style-type:square;">
  <li>For each image file (*.jpg, *.jpeg or *.png) there needs to be exactly one label file (*.xml).</li>
  <li>The size of the images.</li>
  <li>The labels as provided by xml-files.</li> 
</ul>
<p>In case everything is okay, the script shows the following basic output:</p>
<ul style="list-style-type:square;">
  <li>The count of different image shapes.</li>
  <li>The number of images per label.</li>
  <li>A Python label-statement as needed to create the labels for training.</li>
</ul>
<p>In case of no error, the script creates a zip file including all images and labels.</p>

<h2><b>resize_images.py</b></h2> 
<p>Experience shows that high-resolution images are unwieldy for training CNNs. The system will soon run out of memeroy. 
  This scripts takes all images from one folder (e.g. 'original'), resizes them to 1024 x 768 pixel,
and transfers the results to another folder (e.g. 'images'). If an imgae is already smaller than 1024 x 768, the script will just copy it without change. </p> 

<h2><b>prefix_files.py</b></h2> 
<p>This is a pretty simple script that renames all files in a given folder with a prefix. 
  It has proven useful to specify the class name of an image in the file name. This script will help with this.
  The directory name and the desired prefix must be specified in the script.
  The script will not rename files that already have a prefix.
  </p>

<h2><b>analyze_images.py</b></h2> 
<p>This script loads images from a directory and applies image detection to one image at a time. 
  The detection is based on a trained tensorflow-lite CNN model, which needs to be provided via a model folder.
  Accepted image files types are *.jpg, *.jpeg and *.png. 
  Objects found are marked with binding boxes and labels. You can specify a detection threshold (line 43). 
  The keyboard keys a (fast rewind), s (rewind), d (forward), f (fast forward) provide very simple navigation through the image folder. </p>
  <p>The script requiers the class 'detector.py'.</p>
<p>You need to provide the following folders:</p>
<ul style="list-style-type:square;">
  <li>Path to image folder as specified in lines 36 to 38.</li>
  <li>Path to the model folder as specified in ines 39 and 40. The model folder needs to comprise the trained tensorflow lite weights (detect.tflite) and the labels (label.txt).</li>
</ul>

<h2><b>evaluate_image.py</b></h2> 
<p>This scripts evaluates the prediction for a single image. It compares the true objects (as
specified by the annotations) to the estimated objects (as found by the object detector).</p>
<p>Prerequisites:</p>
<ul style="list-style-type:square;">
  <li>a trained tensorflow-lite object detector (tflite.detect and labelmap.txt)</li>
  <li>an image file (filetype .png or .jpg)</li>
  <li>an annotation (label) file (filetype .xml)</li>
</ul>
<p>Image and label files must have the same name (but different endings, obviously)</p>
<p>Output:</p>
<p>(1) list of true objects:</p>
<ul style="list-style-type:square;">
    <li>running index of true object (starting at 0)</li>
    <li>label of the true object</li>
    <li>running index of estimated object (starting at 0)</li>
    <li>label of the estimated object</li>
    <li>score of the estimated object</li>
    <li>factor or the overlap area (intersection)</li>
    <li>match found, overlap > 50% (True or False)</li>
</ul>
<p>(2) list of estimated objects:</p>
<ul style="list-style-type:square;">
    <li>running index of the estimated object (starting at 0)</li>
    <li>label of the estimated object</li>
    <li>score of the estimated object</li>
    <li>match found (True or False)</li>
</ul>
<p>The visualisation shows the true and estimated objects with coloured rectangles.</p>
<ul style="list-style-type:square;">
  <li>green = true object with matching estimated object</li>
  <li>yellow = true object without matching estimated object</li>
  <li>blue = estimated object with matching true object</li>
  <li>red = estimated object without matching true object</li>
</ul>
  
<h2><b>detector.py</b></h2> 
<p>Python class to run the tflite detector.</p>

<h2><b>evaluator.py</b></h2> 
<p>Python class to evaluate the performance of a TensorFlow object detection algorithm.</p>
<p>This class is intended for evaluating the performance of a TensorFLow object detection algorithm.
It compares the predicted objects (= estimated objects) with the labelled objects (= true objects). 
It calculates the intersection area of predicted and labelled objects as a fraction of the estimated area.
A match is determined if the area of an estimated object overlaps the area of the true object by at least 50%.</p>
<p>The most important method of this class is evaluate_img().
This method requires an image file (jpg or png) and a labelling annotation (XML).
It also needs a Tensorflow object detector, which is used to generate the predicted objects.</p>
<p>The method returns two lists:</p>
<ul style="list-style-type:square;">
<li>List (1) contains the true objects and the matches with the predicted objects.</li>
<li>List (2) contains the estimated objects with prediction scores and matches with the true objects.</li>

