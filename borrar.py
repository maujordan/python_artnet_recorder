import csv
from stupidArtnet import StupidArtnet
import time
import glob
import os
import json

path = os.path.dirname(__file__)
recording_path = path + '/recordings'

list_recording_names = glob.glob(recording_path+'/*.csv') # Obteniendo los nombres de los archivos .csv

print(list_recording_names)

