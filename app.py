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
# Paths
dir_path = os.path.dirname(__file__) # Directoro
recordings_path = os.path.join(dir_path, recordings_folder_name)
config_path = os.path.join(dir_path, config_file_name)
states_path = os.path.join(dir_path, states_file_name)
# Json
json_config = get_json_file(config_path) 
json_states = get_json_file(states_path) 

# Ponemos todos los estados en false
for key in list(json_states.keys()):
    change_json_file_value([key], states_path, False)

# Clase de una escena
class scene(BaseModel):
    scene_number: int
    universes: int 

# Creando app para conectarnos
recorder_app = FastAPI()
status_list = []


# Creando petición get para obtener numero de grabaciones y cuantos universos contiene cada una
@recorder_app.get(f'/recordings_info')
def recordings_info(request: Request):
    global states_path
    function_name = inspect.stack()[0][3]

    # Verificamos que este request no se este corriendo
    if get_json_file(states_path)[function_name] == True:
        print("This request is already running, please wait")
        return {"message": "This request is already running, please wait"}
    
    change_json_file_value([function_name], states_path, True)
    recordings_info = get_recordings_info(recordings_path=recordings_path)
    change_json_file_value([function_name], states_path, False)
    return recordings_info


# Creando petición get para reproducir una grabación
@recorder_app.get('/play_recording/{recording_number}')
def read_recording(recording_number: str, request: Request, brackground_tasks: BackgroundTasks):
    
    global states_path
    function_name = inspect.stack()[0][3]
    
    # Revisamos que no se este corriendo ya esta función
    if get_json_file(states_path)[function_name] == True:
        print("This request is already running, please wait")
        return {"message": "This request is already running, please wait"}
    
    # Revisamos que no se este grabando nada
    elif get_json_file(states_path)["new_recording"] == False: 
        change_json_file_value([function_name], states_path, True) # Cambiando estado de los estados a true
        change_json_file_value(level = ["selected_scene"], config_path = config_path, value=recording_number) # Seleccionando escena a reproducir
        brackground_tasks.add_task(broadcast_recording, function_name, states_path) # Reproduciendo escena
        return {"Playing recording:": recording_number}
    
    # Cualquier otro caso es error
    else:
        return {"Error:": "There was an error while trying to read and broadcast recording"}


@recorder_app.post('/new_recording/')
async def new_recording(scene_to_record: scene, request: Request, brackground_tasks: BackgroundTasks):
    function_name = inspect.stack()[0][3]
    global config_path

    # Revisa si el request ya esta corriendo
    if get_json_file(states_path)[function_name] == True : 
        print("There is a scene being recorder, please wait!!!")
        return {"message": "There is a scene being recorder, please wait!!!"}
    
    # revisamos que no se este reproducioendo una grabacion
    elif get_json_file(states_path)[function_name] == False: 
        
        change_json_file_value([function_name], states_path, True)
        scene_to_record = scene_to_record.dict()
        change_json_file_value(level = ["selected_scene"], config_path=config_path, value=scene_to_record["scene_number"])
        change_json_file_value(level = ["settings", "universes"], config_path=config_path, value=scene_to_record["universes"])
        brackground_tasks.add_task(record_artnet)

        return {"message": "Recording..."}
    else:
        return {"error": "Couldn´t record"}

# Cuando hay una grabacion en curso, podemos detenerla
@recorder_app.post('/stop_recording/')
async def stop_recording():
    
    function_name = inspect.stack()[0][3]

    # Begin: manejo de estados
    if get_json_file(states_path)[function_name] == True:
        print("This request is already running, please wait")
        return {"message": "This request is already running, please wait"}
    change_json_file_value([function_name], states_path, True)
    # End: manejo de estados
    
    # Si keep_recording esta en True, cambiamos a False
    if get_json_file(states_path)["new_recording"] == True:
        change_json_file_value(["new_recording"], states_path, False)
        response = {"message": "Stopped recording"}
    else:
        response = {"message": "There is nothing being recorded"}
    
    change_json_file_value([function_name], states_path, False)
    return response

# Para parar una reproducción de escenas
@recorder_app.post('/stop_broadcasting/')
async def stop_broadcasting():
    
    function_name = inspect.stack()[0][3]

    # Revisamos que no se este corriendo la funcion
    if get_json_file(states_path)[function_name] == True:
        print("This request is already running, please wait")
        return {"message": "This request is already running, please wait"}
    else: 
        # Si se esta reproduciendo algo entonces lo paramos
        if get_json_file(states_path)["read_recording"] == True:
            change_json_file_value(["read_recording"], states_path, False)
            response = {"message": "Stopped recording"}
        else:
            response = {"message": "There is nothing being recorded"}

    return response




if __name__ == '__main__':
    uvicorn.run("app:recorder_app", host="0.0.0.0", port=8000, reload=True)
