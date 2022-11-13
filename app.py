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
from main_record_artnet import record_artnet
import uvicorn


# Variables de config
config_file_name = "config.json" # Nombre del config file
recordings_folder_name = "/recordings" # Nombre del recordings folder

dir_path = os.path.dirname(__file__) # Directoro
recordings_path = dir_path + recordings_folder_name
config_path = dir_path + '/' + config_file_name

json_config = json.load(open(os.path.join(dir_path, config_file_name))) # Config json

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
    request_url = request.url.path
    # Verificamos que este request no se este corriendo
    if request_url in status_list:
        print("This request is already running, please wait")
        return {"message": "This request is already running, please wait"}
    status_list.append(request_url) # Agregamos el estado a la lista de estados

    recordings_info = get_recordings_info(recordings_path=recordings_path)
    status_list.remove(request_url) # Quitamos el estado de la lista de estado
    return recordings_info


# Creando petición get para reproducir una grabación
@recorder_app.get('/play_recording/{recording_number}')
def read_recording(recording_number: str, request: Request):
    global status_list
    request_url = request.url.path
    params_no = get_function_number_of_arguments(new_recording)
    # Begin: manejo de estados
    if request_is_running(status_list, request_url, params_no-1):
        print("This request is already running, please wait")
        return {"message": "This request is already running, please wait"}
    status_list = set_request_status(status_list, request_url, params_no-1, running=True) # Cambiamos el estado del request a True
    # End: manejo de estados
    
    change_congig_file_value(level = ["selected_scene"], config_path = config_path, value=recording_number)
    message_to_return = None
    message_to_return = broadcast_recording()
    
    status_list = set_request_status(status_list, request_url, params_no-1, running=False) # Cambiamos el estado del request a False
    return {"recording_to_play": recording_number, "function return": message_to_return}


@recorder_app.post('/new_recording/')
async def new_recording(scene_to_record: scene, request: Request):
    global status_list
    request_url = request.url.path
    params_no = get_function_number_of_arguments(new_recording)
    # Begin: manejo de estados
    if request_is_running(status_list, request_url, params_no-1):
        print("This request is already running, please wait")
        return {"message": "This request is already running, please wait"}
    status_list = set_request_status(status_list, request_url, params_no-1, running=True) # Cambiamos el estado del request a True
    # End: manejo de estados
    
    scene_to_record = scene_to_record.dict()
    change_congig_file_value(level = ["selected_scene"], config_path=config_path, value=scene_to_record["scene_number"])
    change_congig_file_value(level = ["settings", "universes"], config_path=config_path, value=scene_to_record["universes"])
    #record_artnet()
    test_wait()

    status_list = set_request_status(status_list, request_url, params_no-1, running=False) # Cambiamos el estado del request a False
    return

# Cuando hay una grabacion en curso, podemos detenerla
@recorder_app.post('/stop_recording/')
def stop_recording(request: Request):
    global status_list
    request_url = request.url.path
    params_no = get_function_number_of_arguments(new_recording)
    # Begin: manejo de estados
    if request_is_running(status_list, request_url, params_no-1):
        print("This request is already running, please wait")
        return {"message": "This request is already running, please wait"}
    # End: manejo de estados
    
    # Si keep_recording esta en True, cambiamos a False
    if keep_recording(config_path):
        change_congig_file_value(level=["record"], config_path=config_path, value=False)
        response = {"message": "Stopped recording"}
    else:
        response = {"message": "There is no nothing being recorded"}
    
    status_list = set_request_status(status_list, request_url, params_no-1, running=False) # Cambiamos el estado del request a True
    return response
"""
if __name__ == '__main__':
    uvicorn.run(recorder_app, host="0.0.0.0", port=8000)
"""