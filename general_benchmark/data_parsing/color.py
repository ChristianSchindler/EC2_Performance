import os
import matplotlib.colors as mcolors
import cmcrameri.cm as cmc


color = cmc.batlowS


color_dict: dict[str, str] = dict()

# Specify the path to the directory
directory_path = '../../s3/results/2-general_benchmark'

# Get a list of all items (files and folders) in the directory
folder_paths = os.listdir(directory_path)
i = 0
for instance_name in folder_paths:
    color_dict[instance_name] = color(i)
    i += 1

print(color_dict)