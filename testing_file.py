import os

from utils.utils import *
go_on = 1

def testing_function(config_path):
    global go_on
    
    while go_on == 1:
        print("Seguimos grabando")
        go_on = keep_recording(config_path=config_path)
        if go_on == 0:
            print("\nParamos grabacion")

    return

dirname = os.path.dirname(__file__)
config_file_name = 'config.json'
config_path = dirname + '/' + config_file_name

testing_function(config_path)