""" detector.py

Class to run tensorflow object detection from a trained network.
The model data must be provided in a directory <model> that comprises the files "detect.tflite" and "labelmap.txt". 
Based on Google tensorflow examples and tutorials with minor modifications.

Methods:
- detect_objects() - applies the detector to an image
- add_box() - adds a rectangle including label to an image

Dependencies: OpenCV, tensorflow lite

SLW 2023
"""

import os
import cv2
import numpy as np

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Raspberry Pi
# from tflite_runtime.interpreter import Interpreter

# Windows
import tensorflow.lite
Interpreter = tensorflow.lite.Interpreter

class Detector:
    def __init__(self, model_dir, verbose=True):
        # Operating values
        self.__labels = []
        self.__verbose = verbose
        self.model_dir = model_dir
        self.interpreter = Interpreter(os.path.join(model_dir, "detect.tflite"))
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.interpreter_height = self.input_details[0]['shape'][1]
        self.interpreter_width = self.input_details[0]['shape'][2]
        self.model_type = self.input_details[0]['dtype']
        if verbose:
            print("Interpreter resolution:", self.interpreter_width, 'x', self.interpreter_height)
            print("Interpreter type:", self.model_type)
        self.output_details = self.interpreter.get_output_details()
        self.input_mean, self.input_std = 255/2, 255/2
        self.model_is_float = (self.model_type == np.float32)
        self.outname = self.output_details[0]['name']
        if ('StatefulPartitionedCall' in self.outname): # TF2 model
            self.boxes_idx, self.classes_idx, self.scores_idx = 1, 3, 0
        else: # TF1 model
            self.boxes_idx, self.classes_idx, self.scores_idx = 0, 1, 2
        self._read_labels()

                
    def _read_labels(self):
        path_to_labelmap = os.path.join(self.model_dir, "labelmap.txt")
        with open(path_to_labelmap, 'r') as f:
            lines = f.readlines()
            labels = [l.strip() for l in lines]
            if labels[0] == "???":
                del(labels[0])
            self.__labels = labels
            if self.__verbose:
                print(len(labels), "labels found")
                print()
            
            
    def detect_objects(self, frame):
        """ Takes a cv2 image frame and returns 10 identified objects.
            The return includes three lists:
                binding boxes (x/y coordinates)
                classes (int)
                probability scores (0.0 - 1.0)
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (self.interpreter_width, self.interpreter_height))
        input_data = np.expand_dims(frame_resized, axis=0)
        if self.model_is_float:
            input_data = (np.float32(input_data) - self.input_mean) / self.input_std
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        boxes = self.interpreter.get_tensor(self.output_details[self.boxes_idx]['index'])[0]
        classes = self.interpreter.get_tensor(self.output_details[self.classes_idx]['index'])[0]
        classes = [int(c) for c in classes]
        scores = self.interpreter.get_tensor(self.output_details[self.scores_idx]['index'])[0]
        return boxes, classes, scores
        
        
    def add_box(self, frame, box, label, color=(0, 255, 0), thickness=2):
        """ Adds a rectangle to an image.
            - 'box' is a tuple of 4 float values specifying the position (ymin, xmin, ymax, xmax)
            - 'label' is text that will be written on top of the rectangle.
            - 'color' is a tuple of RGB values specifying the color of the box. """
        height, width = frame.shape[:2]
        # Draw rectangle
        ymin = int(max(1,(box[0] * height)))
        xmin = int(max(1,(box[1] * width)))
        ymax = int(min(height,(box[2] * height)))
        xmax = int(min(width,(box[3] * width)))  
        cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), color, thickness)
        # Draw label
        if len(label) > 0:
            label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2) 
            label_ymin = max(ymin, label_size[1] + 10) # Make sure not to draw label too close to top of window
            cv2.rectangle(frame,
                            (xmin, label_ymin-label_size[1]-10),
                            (xmin+label_size[0], label_ymin+base_line-10),
                            (255, 255, 255), cv2.FILLED) 
            cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        return frame
        

    @property
    def labels(self):
        return self.__labels
    

#====================================================================================

if __name__ == "__main__":
    
    # Files and directories
    image = "paramecium_caudatum_Snap-620.jpg"
    project_dir = "micro-organisms"
    image_dir = "images"
    model_dir = "model"
    threshold = 0.5
    
    # Run detector
    dtc = Detector(os.path.join(project_dir, model_dir))
    img = cv2.imread(os.path.join(project_dir, image_dir, image))
    boxes, classes, scores = dtc.detect_objects(img)
    
    # Add boxes to image
    for i in range(10):
        if scores[i] > threshold:
            img = dtc.add_box(img, boxes[i],
                              dtc.labels[classes[i]] + ": " + str(round(scores[i]*100)) + '%')
        else:
            break
    
    # Show the image and wait for a key
    cv2.imshow("", img)
    key = cv2.waitKey(0) & 0xff
    
    # Cleanup
    cv2.destroyAllWindows()
    
