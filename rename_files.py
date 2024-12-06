""" rename_files.py

A pretty simple script that renames all files in a folder with a prefix.

SLW 12-2024
"""

import os

# Directories
project_dir = "things"
image_dir = "images_xyz"
image_path = os.path.join(project_dir, image_dir) 

# Prefix
prefix = "new"
prefix_len = len(prefix)

print("Renameing files in " + image_path)
files = os.listdir(image_path)
cnt = 0
skipped = 0
if len(files) == 0:
    print("The folder is empty!!!")
else:
    for name in files:
        if len(name) < prefix_len or name[:prefix_len+1] != (prefix + '_'):
            new_name = prefix + '_' + name
            os.rename(os.path.join(image_path, name), os.path.join(image_path, new_name))
            cnt += 1
        else:
            skipped += 1
            
    
print(cnt, "files renamed")
print(skipped, "files skipped")
print("Done!")
print()
