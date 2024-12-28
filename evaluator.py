""" evaluator.py

This class is intended for evaluating the performance of a TensorFLow object detection algorithm.
It compares the predicted objects (= estimated objects) with the labelled objects (= true objects). 
It calculates the intersection area of predicted and labelled objects as a fraction of the estimated area.
A match is determined if the area of an estimated object overlaps the area of the true object by at least 50%.

The most important method of this class is 'evaluate_img()'.
This method requires an image file (jpg or png) and a labelling annotation (XML).
It also needs a Tensorflow object detector, which is used to generate the predicted objects.
The method returns:
    (1) List of true objects and the matches with the predicted objects.
    (2) List of estimated objects with prediction scores and matches with the true objects.
    (3) If visualization is on: key pressed, otherwise: 0

SLW Dec-2024
"""

import os
import cv2
import detector

class Evaluator:
    
    def __init__(self, model_path):
        self._dtc = detector.Detector(model_path, verbose=False)
        # Colors
        self._green = (0, 255, 0)     # true box with match
        self._yellow = (0, 255, 255)  # true box without match
        self._red = (0, 0, 255)       # estimated box with match
        self._blue = (255, 0, 0)      # estimated box without match
        
            
    def _extract_tag(self, s, tag):
        """ Extracts a single tag from an XML string """
        start_pos = s.find("<" + tag + ">")
        end_pos = s.find("</" + tag + ">")
        if start_pos < 0 or end_pos < start_pos:
            return "", -1
        label = s[start_pos + len(tag) + 2 : end_pos]
        return label, end_pos + len(tag) + 3
        
        
    def _decode_xml(self, filename, image_path):
        """ Decodes XML label files, returns image filename, classes and boxes """
        filename_details = filename.split('.')
        if len(filename_details) == 1:
            filename += '.xml'
        else:
            if filename_details[1].casefold() != "xml".casefold():
                print("Error: decode_xml - xml file expected, '" + filename + "' received!")
                return "none", [], []
        with open(os.path.join(image_path, filename), "r") as xml_file:
            s = xml_file.read()
        # Extract image filename
        img_filename, pos = self._extract_tag(s, "filename")
        if len(img_filename) == 0 or pos <= 0:
            print("Error: decode_xml - can't find filename-tag!")
            return "none", [], []
        s = s[pos :]
        # Extract width and height
        width, pos = self._extract_tag(s, "width")
        if len(width) == 0 or pos <= 0:
            print("Error: decode_xml - can't find width-tag!")
            return "none", [], []
        width = int(width)
        s = s[pos :]
        height, pos = self._extract_tag(s, "height")
        if len(height) == 0 or pos <= 0:
            print("Error: decode_xml - can't find height-tag!")
            return "none", [], []
        height = int(height)
        s = s[pos :]  
        # Extract classes and boxes
        classes = []
        boxes = []
        while True:
            class_name, pos = self._extract_tag(s, "name")
            if len(class_name) == 0 or pos <= 0:
                break
            classes.append(class_name)
            s = s[pos : ]
            xmin, pos = self._extract_tag(s, "xmin")
            if len(xmin) == 0 or pos <= 0:
                print("Error: decode_xml - can't find xmin-tag!")
                break
            s = s[pos : ]
            ymin, pos = self._extract_tag(s, "ymin")
            if len(ymin) == 0 or pos <= 0:
                print("Error: decode_xml - can't find ymin-tag!")
                break
            s = s[pos : ]
            xmax, pos = self._extract_tag(s, "xmax")
            if len(xmax) == 0 or pos <= 0:
                print("Error: decode_xml - can't find xmax-tag!")
                break
            s = s[pos : ]
            ymax, pos = self._extract_tag(s, "ymax")
            if len(ymin) < 0 or pos <= 0:
                print("Error: decode_xml - can't find ymax-tag!")
                break
            box = (int(ymin) / height, int(xmin) / width,
                   int(ymax) / height, int(xmax) / width)
            boxes.append(box)
            
        return img_filename, classes, boxes
    
    
    def evaluate_img(self, filename, image_path, verbose=False, show_img=False,
                     probability_threshold = 0.5, intersection_threshold = 0.5):
        """ Evaluates an image based on a comparison of labeled (true) objects and estimated objects.
            It searches matches and calculates the intersection area as a fraction of the estimated box.
            If desired, the function plots an image including boxes.
            The function returns:
            (1) list of true objects:
            - index of true object
            - label of true object
            - index of estimated object
            - label of estimated object
            - score of estimated object
            - factor or covered area
            - match found (True or False)
            (2) list of estimated objects:
            - index of the estimated object
            - label of the estimated object
            - score of the estimated object
            - match found (True or False)
            (3) if visualization is on: key pressed, otherwise: 0
        """

        fname = "evaluate_img: "

        # Decode XML file and get true objects
        img_filename, true_classes, true_boxes = self._decode_xml(filename + '.XML', image_path)
        if img_filename == "none":
            print(fname + "Error: files not found: " + filename)
            return [], []

        # Loading the image file
        if verbose:
            print(fname + "processing file '" + img_filename + "'")
            print(fname + str(len(true_classes)) + " true objects found")
        
        # Get estimations from detector and add estimated boxes to images
        true_lst = []
        img = cv2.imread(os.path.join(image_path, img_filename))
        est_boxes, est_classes, est_scores = self._dtc.detect_objects(img)   
        for idx in range(10):
            if est_scores[idx] < probability_threshold:
                break
        est_boxes = est_boxes[:idx]
        est_classes = est_classes[:idx]
        est_scores = est_scores[:idx]
        est_matches = [False for ec in est_classes]
        est_labels = [self._dtc.labels[ec] for ec in est_classes]
        est_areas = [(b[2] - b[0]) * (b[3] - b[1]) for b in est_boxes]
        if verbose:
            print(fname + str(len(est_classes)) + " estimated objects found")
        
        # Walk through true objects and find matches
        for true_idx, tc in enumerate(true_classes):
            true_details = [true_idx, tc]
            true_box = true_boxes[true_idx]
            if verbose:
                print(fname + "working on object " + str(true_idx) + ", " + tc)
            
            # Match true object against all estimators and calculate intersection
            local_intersections = [0 for i in range(len(est_classes))]
            for est_idx, ec in enumerate(est_labels):
                verbose_str = fname + "  - estimator object " + str(est_idx) + ", " + ec
                est_box = est_boxes[est_idx]
                inter_ymin = max(est_box[0], true_box[0])
                inter_xmin = max(est_box[1], true_box[1])
                inter_ymax = min(est_box[2], true_box[2])
                inter_xmax = min(est_box[3], true_box[3])
                if (inter_ymax > inter_ymin) and (inter_xmax > inter_xmin):
                    inter_area = (inter_ymax - inter_ymin) * (inter_xmax - inter_xmin)
                    factor = inter_area / est_areas[est_idx]
                    local_intersections[est_idx] = factor
                    verbose_str += " - factor: " + str(round(factor, 3))
                else:
                    verbose_str += " - no intersection"
                if verbose:
                    print(verbose_str)
                    
            # Find maximum in local intersections
            local_max = 0
            est_idx = -1
            for idx, local_inter_factor in enumerate(local_intersections):
                if local_inter_factor > local_max:
                    local_max = local_inter_factor
                    est_idx = idx
            
            # Generate output vector for true objects based on results
            if est_idx >= 0:
                true_details += [est_idx, est_labels[est_idx], est_scores[est_idx],
                                 local_max, local_max > intersection_threshold]
                est_matches[est_idx] = True
            else:
                true_details += [-1, "", 0.0, 0.0, False]
            true_lst.append(true_details)
            
        # Generate output list for estimated objects
        est_lst = []
        for est_idx, ec in enumerate(est_labels):
            est_lst.append([est_idx, ec, est_scores[est_idx], est_matches[est_idx]])
                
        if verbose:
            print()
            print(fname + "true objects:")
            for to in true_lst:
                print(fname + " - " + str(to))
            print(fname + "estimated objects:")
            for eo in est_lst:
                print(fname + " - " + str(eo))
            print()
        
        # Show image
        key = 0
        if show_img:
            # Add true boxes to images
            for idx, to in enumerate(true_lst):
                if to[6]:
                    flag = "okay" if to[1] == to[3] else "wrong"
                    img = self._dtc.add_box(img, true_boxes[idx], to[1] + " (" + flag + ")", self._green)
                else:
                    img = self._dtc.add_box(img, true_boxes[idx], to[1] + " (not found)", self._yellow)               
            # Add estimatores to image
            for idx, eo in enumerate(est_lst):
                if eo[3]:
                    img = self._dtc.add_box(img, est_boxes[idx], "", self._blue)
                else:
                    img = self._dtc.add_box(img, est_boxes[idx], "", self._red)
                    
            # Show the image and wait for the keyboard
            cv2.imshow("", img)
            key = cv2.waitKey(0) & 0xff
        
        return true_lst, est_lst, key
    
    
    def cleanup(self):
        cv2.destroyAllWindows()
        

#===================================================================================================
    
if __name__ == "__main__":
    
    print("Evaluate a single image")
    print(40 * "=")

    # Directory and file definitions
    image = "Snap-846"
    project_dir = "micro-organisms"
    image_dir = "images"
    image_file_list = "test_images.txt"
    model_dir = "model"

    # Directories
    image_path = os.path.join(project_dir, image_dir)
    model_path = os.path.join(project_dir, model_dir)
    
    # Evaluater
    evl = Evaluator(model_path)
    true_lst, est_lst, _ = evl.evaluate_img(image, image_path, verbose=False, show_img=True)

    # Show results
    print("True objects")
    for true_obj in true_lst:
        print(true_obj)
    print("Estimated objects")
    for est_obj in est_lst:
        print(est_obj)

    # We are done
    evl.cleanup()
    print("Done!")
