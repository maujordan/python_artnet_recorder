# uvicorn app:app --> Inicia el servidor de nombre app
# uvicorn app:app --reload --> Cada vez que guarda el archivo refresca el servidor uvicorn 
# 

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


# Declarando templates
templates = Jinja2Templates(directory="templates")


# Files and folders names
config_file_name = "config.json" # Nombre del config file
descriptions_file_name = "descriptions.json" # Nombre del file que contiene descrpciones de las grabaciones
recordings_folder_name = "recordings" # Nombre del recordings folder
states_file_name = "states.json" # ombre del archivo que guarda estados
static_folder_name = "static"

# Paths
dir_path = os.path.abspath('')
recordings_path = os.path.join(dir_path, recordings_folder_name) 
config_path = os.path.join(dir_path, config_file_name)
states_path = os.path.join(dir_path, states_file_name)
static_folder_path = os.path.join(dir_path, static_folder_name)
descriptions_path = os.path.join(dir_path, descriptions_file_name)
# Json
json_config = get_json_file(config_path) 
json_states = get_json_file(states_path) 

#Checking that necessary files exist before running
create_folder_if_it_doesnt_exist(recordings_path)


# Ponemos todos los estados en false
for key in list(json_states.keys()):
    change_json_file_value([key], states_path, False)

# Clase de una escena
class scene(BaseModel):
    scene_number: int
    universes: int 

class config_change(BaseModel):
    lista_campo: list
    value: str


# Creando app para conectarnos
recorder_app = FastAPI()
# Agregando directorio estatico donde guardamos los css y jquery
recorder_app.mount(
    "/static",
    StaticFiles(directory=static_folder_path, html=True),
    name="static",
)
status_list = []




# Home
@recorder_app.get(f'/')
def home_page(request: Request):
    """
    Displays the main page of the webserver
    """

    direccion_ip = get_ip_address()

    return templates.TemplateResponse("home.html", {
        "request": request,
        "ip_address": direccion_ip
    })
    
# Broadcast scene page
@recorder_app.get(f'/broadcast_page')
def broadcast_page(request: Request):
    """
    Displays de broadcast section
    """
    
    recordings_details = get_recordings_info(recordings_path, descriptions_path)
    recordings_info = recordings_details["content"] # Obteniendo informacion de cuantos universos hay por escena
    recordings_descriptions = recordings_details["descriptions"] # Obteniendo descripciones de escenas
    
    # Obteniendo las grabaciones que tienen mas de 0 universos
    non_empty_recordings_list = []
    for k in recordings_info.keys():
        non_empty_recordings_list.append(f"Recording: { k }") if recordings_info[k] > 0 else None


    return templates.TemplateResponse("broadcast.html", {
        "request": request,
        "recordings_info": recordings_info,
        "recordings_descriptions": recordings_descriptions
    })


# Record page
@recorder_app.get(f'/record_page')
def record_page(request: Request):
    """
    Displays the recording new scenes page
    Here you the user is able to record new scenes
    """
    scenes_to_display = 40
    recordings_info = get_recordings_info(recordings_path)["content"]
    # Creando diccionario con n cantidad de posibles escenas para grabar
    scenes = {}
    
    for s in range(scenes_to_display):
        # Revisando si la grabacion tiene contenido, si tiene contenido, almacenamos cuantos universos tiene
        if str(s) in list(recordings_info.keys()):
            scenes[s] = recordings_info[str(s)]
        else:
            scenes[s] = 0
    
    return templates.TemplateResponse("record_scene_page.html", {
        "request": request,
        "scenes_info": scenes
    })
    


# Creando petición get para obtener numero de grabaciones y cuantos universos contiene cada una
@recorder_app.get(f'/recordings_info')
def recordings_info(request: Request):
    global states_path
    function_name = inspect.stack()[0][3]

    # Verificamos que este request no se este corriendo
    if get_json_file(states_path)[function_name] == True:
        print("This request is already running, please wait")
        return {"message": "This request is already running, please wait"}
    
    change_json_file_value([function_name], states_path, True) # Cambiamos estado de funcion
    recordings_info = get_recordings_info(recordings_path=recordings_path)
    change_json_file_value([function_name], states_path, False) # Cambiamos estado de función
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
        # Si hay 0 universos en el folder, no corremos funcion
        if get_number_of_universes_in_recording(recordings_path + f'/scene_{ recording_number }') == 0:
            change_json_file_value([function_name], states_path, False) # Cambiando estado de los estados a true
            return {"message":{"There´s nothing in:": f"scene_{ recording_number }"}}

        brackground_tasks.add_task(broadcast_recording, function_name, states_path) # Reproduciendo escena
        return {"message":{"Playing recording:": recording_number}}
    
    # Cualquier otro caso es error
    else:
        change_json_file_value([function_name], states_path, False) # Cambiando estado de reproducción
        return {"message": {"Error:": "There was an error while trying to read and broadcast recording"}}


@recorder_app.post('/new_recording/')
async def new_recording(scene_to_record: scene, request: Request, brackground_tasks: BackgroundTasks):
    function_name = inspect.stack()[0][3]
    global config_path

    # Revisa si el request ya esta corriendo
    if get_json_file(states_path)[function_name] == True : 
        print("There is a scene being recorded, please wait!!!")
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
    
    # Si keep_recording esta en True, cambiamos a False
    if get_json_file(states_path)["new_recording"] == True:
        change_json_file_value(["new_recording"], states_path, False)
        response = {"message": "Stopped recording"}
    else:
        response = {"message": "There is nothing being recorded"}
    
    return response


# Para parar una reproducción de escenas
@recorder_app.post('/stop_broadcasting/')
async def stop_broadcasting():
    
    function_name = inspect.stack()[0][3]

    # Si se esta reproduciendo algo entonces lo paramos
    if get_json_file(states_path)["read_recording"] == True:
        change_json_file_value(["read_recording"], states_path, False)
        response = {"message": "Stopped broadcasting"}
    else:
        response = {"message": "There is nothing being broadcasted"}

    return response


# Cambia un valor del config.json
@recorder_app.post('/change_config_value/')
async def endpoint_change_config_value(field_to_change: config_change):
    """
    Cambia algun valor del config file
    """
    function_name = inspect.stack()[0][3]
    # Manejo de estados
    # Si ya esta corriendo no ejecutamos
    if get_json_file(states_path)[function_name] == True: 
        return {"message": "This request is already running, please wait"}
    # si no esta corriendo ejecutamos
    else:
        change_json_file_value([function_name], states_path, True) # estado running
        change_json_file_value(field_to_change.lista_campo, config_path, field_to_change.value) # Cambiando la ip
        change_json_file_value([function_name], states_path, False) # estado not running

    return {"message": f"Succesfully changed '{ field_to_change.lista_campo[-1] }' field to '{ field_to_change.value }'"}


# Busca los dispositivos conectados  la red
class NetworkDevice(BaseModel):
    ip_address: str
    ac_address: str

@recorder_app.get('/find_devices_on_network/')
async def find_devices_on_network():
    """
    ARREGLAR
    Corre un "arp -a" para buscar los dispositivos conectados a la red.
    Returns: lista con listas [[ip1, mac1], [ip2, mac2]]
    """
    
    """
    # Manejo de estados
    # Si ya esta corriendo no ejecutamos
    function_name = inspect.stack()[0][3]
    if get_json_file(states_path)[function_name] == True: 
        return {"message": "This request is already running, please wait"}
    # si no esta corriendo ejecutamos
    else:
        change_json_file_value([function_name], states_path, True) # estado running
        # Aqui ejecutamos las acciones
        devices_on_network = find_devices_on_network()
        change_json_file_value([function_name], states_path, False) # estado not running

    return {"message": devices_on_network}
    """


@recorder_app.delete('/delete_scene/{scene_to_delete}')
def delete_scene_endpoint(scene_to_delete: int):
    """
    Elimina alguna escena que este grabada
    Recibe la escena a eliminar a manera de int.
    """
    result = delete_scene(recordings_path, f"scene_{ scene_to_delete }")
    result = 1
    if result == 1:
        return {"message": f"scene_{ scene_to_delete } deleted!"}
    elif result == 0:
        return {"message": f"Couldn´t delete. scene_{ scene_to_delete } doesn´t exist yet!"}
    else:
        return {"ERROR"}


class update_body(BaseModel):
    scene_to_update: str
    description_message: str
@recorder_app.post('/update_recording_description/')
def update_recording_description(update_info: update_body):

    update_description_file(update_info.scene_to_update, text_to_place=update_info.description_message)    

    return {"message": f"Updated description for scene '{ update_info.scene_to_update }' to: { update_info.description_message }"}
    

class update_wifi_body(BaseModel):
    SSID: str
    wifi_password: str
@recorder_app.post('/change_wifi_settings/')
def change_wifi_settings(wifi_credentials: update_wifi_body):
    """
    Changes the wifi SSID and password. Before running the permissions of the file have to be changed have to be changed running: sudo chmod 777 /etc/wpa_supplicant/wpa_supplicant.conf.
    Reboots in at the end.
    Parameters:
        - SSID
        - password
    Returns: null
    """

    print(wifi_credentials.SSID, wifi_credentials.wifi_password)
    CreateWifiConfig(wifi_credentials.SSID, wifi_credentials.wifi_password)

    return

# Corriendo app
if __name__ == '__main__':
    uvicorn.run("app:recorder_app", host="0.0.0.0", port=8000, reload=True)
    #uvicorn.run("app:recorder_app", host="0.0.0.0", port=8000)