# uvicorn app:app --> Inicia el servidor de nombre app
# uvicorn app:app --reload --> Cada vez que guarda el archivo refresca el servidor uvicorn 

from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
from typing import Text, Optional # Objetos de tipo texto
from datetime import datetime
from uuid import uuid4 as uuid
from main_send_recording import broadcast_recording
from inspect import signature
from main_record_artnet import record_artnet
import time
import asyncio
import uvicorn
import inspect
# User functions
from utils.utils import *
from testing_file import * 


# Files and folders names
config_file_name = "config.json" # Nombre del config file
recordings_folder_name = "recordings" # Nombre del recordings folder
states_file_name = "states.json" # ombre del archivo que guarda estados

dir_path = os.path.dirname(__file__) # Directoro
recordings_path = os.path.join(dir_path, recordings_folder_name)
config_path = os.path.join(dir_path, config_file_name)
states_path = os.path.join(dir_path, states_file_name)

change_json_file_value(["recordings_info"], states_path, True)