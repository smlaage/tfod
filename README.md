<t>This is a loose collection of helpful scripts to support tensorflow image detection.</t>
SLW - Oct 2024

<p><b>check_images.py</b>: This scripts checks labeled images in preparation 
for the use in tensor flow training. It checks the following topics:</p>
<ul style="list-style-type:square;">
  <li>For each image file (*.jpg, *.jpeg or *.png) there needs to be exactly one label file (*.xml)</li>
  <li>The size of the images</li>
  <li>The labels as provided by xml-files</li> 
<p>In case everything is okay, the shows basic statistics:</p>
<ul style="list-style-type:square;">
  <li>the count of different image shapes</li>
  <li>the number of images per label</li>
  <li>a Python label-statement as needed to create the labels for training</li>
<p>in case of no error, the script creates a zip file including all images and labels.</p>
