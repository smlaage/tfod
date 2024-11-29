""" detector.py

Class to run tensorflow object detection applying a trained model.
The model data must be provided in a directory <model> that comprises the files "detect.tflite" and "labelmap.txt". 
Based on Google tensorflow examples and tutorials with minor modifications

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
    def __init__(self, model_dir):
        self.model_dir = model_dir
        self.__labels = []
        self.interpreter = Interpreter(os.path.join(model_dir, "detect.tflite"))
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.interpreter_height = self.input_details[0]['shape'][1]
        self.interpreter_width = self.input_details[0]['shape'][2]
        self.model_type = self.input_details[0]['dtype']
        print("Interpreter resolution:", self.interpreter_width, 'x', self.interpreter_height)
        print("Interpreter type:", self.model_type)
        self.output_details = self.interpreter.get_output_details()
        self.input_mean = 255/2
        self.input_std = 255/2
        self.model_is_float = (self.model_type == np.float32)
        self.outname = self.output_details[0]['name']
        if ('StatefulPartitionedCall' in self.outname): # TF2 model
            self.boxes_idx, self.classes_idx, self.scores_idx = 1, 3, 0
        else: # TF1 model
            self.boxes_idx, self.classes_idx, self.scores_idx = 0, 1, 2
        self.read_labels()
        
                
    def read_labels(self):
        path_to_labelmap = os.path.join(self.model_dir, "labelmap.txt")
        with open(path_to_labelmap, 'r') as f:
            lines = f.readlines()
            labels = [l.strip() for l in lines]
            if labels[0] == "???":
                del(labels[0])
            self.__labels = labels
            print(len(labels), "labels found")
            
            
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
        scores = self.interpreter.get_tensor(self.output_details[self.scores_idx]['index'])[0]
        classes = [int(c) for c in classes]
        return boxes, classes, scores
    
    
    @property
    def labels(self):
        return self.__labels
