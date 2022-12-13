from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import inspect
# User functions
from main_send_recording import broadcast_recording
from main_record_artnet import record_artnet
from utils.utils import *


# Files and folders names
config_file_name = "config.json" # Nombre del config file
recordings_folder_name = "recordings" # Nombre del recordings folder
states_file_name = "states.json" # ombre del archivo que guarda estados
static_folder_name = "static"
# Paths
dir_path = os.path.dirname(__file__) # Directoro
recordings_path = os.path.join(dir_path, recordings_folder_name) 
config_path = os.path.join(dir_path, config_file_name)
states_path = os.path.join(dir_path, states_file_name)
static_folder_path = os.path.join(dir_path, static_folder_name)
# Json
json_config = get_json_file(config_path) 
json_states = get_json_file(states_path) 

json_config