""" evaluate_image_list.py

SLW Oct-2024 - Dec-2024
"""

import os
import pandas as pd
import evaluator

# Set files and paths
project_dir = "micro-organisms"
image_dir = "images"
image_file_lists = ["train_images.txt", "test_images.txt"]
model_dir = "model"

print("Evaluate image lists")
print(40 * "=")
print()

# Directories
image_path = os.path.join(project_dir, image_dir)
model_path = os.path.join(project_dir, model_dir)

# Start evaluator
evl = evaluator.Evaluator(model_path)

# Evaluate the lists of images
for file_list in image_file_lists:

    # Create dataframes to capture the results
    true_results = pd.DataFrame(columns = ['image', 'true_idx', 'true_label', 'est_idx', 'est_label', 'score', 'intersection', 'match'])
    est_results = pd.DataFrame(columns = ['image', 'est_idx', 'est_label', 'score', 'match'])
    true_row_idx = 0
    est_row_idx = 0

    # Open image file list
    with open(os.path.join(project_dir, file_list), "r") as files:
        img_lst = files.readlines()
    if len(img_lst) == 0:
        print("File list is empty. Nothing to do!")
        print()
        continue
        
    # Work on image by image
    print()
    print("Evaluating images ...")
    for image_file in img_lst:
        image_file = image_file.strip('\n')
        pos = image_file.rfind('/')
        if pos > 0:
            image_file = image_file[pos + 1 :]
        pos = image_file.rfind('.')
        if pos < 0:
            print("Error: can't identify file type on '" + image_file + "'. File skipped.")
            continue
        image_name = image_file[: pos]
        image_filetype = image_file[pos+1 : ]
        if image_filetype.casefold() == "xml".casefold():
            print("- " + image_name + 20 * ' ', end='\r')
            # Get true and estimated objects
            true_lst, est_lst, _ = evl.evaluate_img(image_name, image_path, verbose=False, show_img=False)
            # Add findings to dataframes
            for true_obj in true_lst:
                true_results.loc[true_row_idx] = [image_name] + true_obj
                true_row_idx += 1
            for est_obj in est_lst:
                est_results.loc[est_row_idx] = [image_name] + est_obj
                est_row_idx += 1

    # Clean up
    print("Done!" + 20 * ' ')
    evl.cleanup()

    # Show summary
    print()
    print("Summary for '" + file_list + "'")
    print((14 + len(file_list)) * '=')
    print()
    true_cnt = len(true_results)
    matches = true_results['match'].count()
    correct = true_results[true_results['true_label'] == true_results['est_label']]['image'].count()
    localization = true_results['intersection'].sum()
    est_cnt = len(est_results)
    matchless = est_results[est_results['match'] == False]['est_idx'].count()
    print("All classes " + 62 * '-')
    title_str = "True Obj     Matches  Correct Matches  Localization  Est.Obj  Not Matching"
    print(title_str)
    if true_cnt > 0 and matches > 0 and est_cnt > 0:
        print("   {:5d}{:5d}/{:5.1f}%     {:5d}/{:5.1f}%        {:5.1f}%    {:5d}  {:5d}/{:5.1f}%".format(
            true_cnt, matches, matches*100/true_cnt, correct, correct*100/true_cnt, 
            localization*100/matches, est_cnt, matchless, matchless*100/est_cnt))
    else:
        print("   {:5d}           -                -             -    {:5d}             -".format(
            true_cnt, est_cnt))
            
    print()

    print("By class " + 85 * '-')
    print("Class               " + title_str)
    class_lst = true_results['true_label'].value_counts()
    for c in class_lst.index:
        true_results_byclass = true_results[true_results['true_label'] == c]
        true_cnt = len(true_results_byclass)
        matches = true_results_byclass['match'].count()
        correct = true_results_byclass[true_results_byclass['true_label'] == true_results_byclass['est_label']]['image'].count()
        localization = true_results_byclass['intersection'].sum()
        est_results_byclass = est_results[est_results['est_label'] == c]
        est_cnt = len(est_results_byclass)
        matchless = est_results_byclass[est_results_byclass['match'] == False]['est_idx'].count()
        if true_cnt > 0 and matches > 0 and est_cnt > 0:
            print("{:20s}   {:5d}{:5d}/{:5.1f}%     {:5d}/{:5.1f}%        {:5.1f}%    {:5d}  {:5d}/{:5.1f}%".format(
                c, true_cnt, matches, matches*100/true_cnt, correct, correct*100/true_cnt, 
                localization*100/matches, est_cnt, matchless, matchless*100/est_cnt))
        else:
            print("{:20s}   {:5d}           -                -             -    {:5d}             -".format(
                c, true_cnt, est_cnt))

            
    print()
    
print(40 * '-')    
print("Test images with the highest number of errors:")
true_results_nomatch = true_results[true_results['match'] == False]
if len(true_results_nomatch) == 0:
    print("None!")
else:
    print(true_results_nomatch['image'].value_counts().head(10))
print()
    
print("Done!")

