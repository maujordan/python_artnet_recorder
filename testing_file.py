import os

dirname = os.path.dirname(__file__) + "/"


recordings_path_name = "recordings"

selected_scene = 1

########### 
scene_directory = dirname + recordings_path_name + f"/scene_{ selected_scene }"
lst = os.listdir(scene_directory) # your directory path
number_universes_in_scene = len(lst)