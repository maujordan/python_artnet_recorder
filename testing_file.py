from stupidArtnet import StupidArtnetServer
import json
import os
from csv import writer
import sys
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=False) # Errores en color

# Path to save the recordings
# recordings_path = '/home/maurojordan/Documents/python_artnet_recorder/recordings'

# Files de configuracion
dirname = os.path.dirname(__file__)
data = json.load(open(os.path.join(dirname, 'config.json')))
selected_scene = data['selected_scene'] # Escena a grabar
recordings_path = dirname + f"/recordings/scene_{ selected_scene }" 




import os

# Check whether the specified path exists or not

path = os.path.dirname(__file__) # Path en el que estamos
data = json.load(open(os.path.join(path, 'config.json')))
selected_scene = data['selected_scene'] # Escena a grabar
recordings_path = dirname + f"/recordings/scene_{ selected_scene }"  # Path donde se encuentran los recordings


recording_path_exists = os.path.exists(recordings_path) # verificando si el path existe
if recording_path_exists == False:
    print(f"La grabacion { selected_scene } no existe. Por favor crearla")
    exit()