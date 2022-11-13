# uvicorn app:app --> Inicia el servidor de nombre app
# uvicorn app:app --reload --> Cada vez que guarda el archivo refresca el servidor uvicorn 

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Text, Optional # Objetos de tipo texto
from datetime import datetime
from uuid import uuid4 as uuid
from utils.utils import *
from main_send_recording import broadcast_recording
from inspect import signature


dirname = os.path.dirname(__file__)
config_file_name = 'config.json'
config_path = dirname + '/' + config_file_name
config_path = os.path.join(dirname, config_file_name)

# Funcion que lee del config si seguimos grabando
def keep_recording(config_path: str):
    # Files de configuracion
    data = json.load(open(config_path))
    return data["record"]

print(keep_recording(config_path))