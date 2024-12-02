<t>This is a loose collection of helpful Python scripts to support tensorflow object detection.</t>
<p>The recommended folder structure is shown in "folder_structrue.png".</p>
<p>Dependecies:</p>
<ul style="list-style-type:square;">
  <li>Windows: tensorflow.lite (this is incldued in the full tensorflow package)</li>
  <li>Raspberry Pi: tflite_runtime.interpreter</li>
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

<h2><b>detector.py</b></h2> 
<p>Python class to run the tflite detector.</p>

