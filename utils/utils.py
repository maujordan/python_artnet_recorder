import os
import json
import time


# Funcion para cambiar algun valor del config.json
    # Recibe: elemento que vamos a cambiar en una lista, el config file path y el valor que vamos que insertaremos
def change_congig_file_value(level:list, config_path:str, value):
    try:
        # Obteniendo nombre de directorio
        config_path = "config.json"

        # Leyendo config file y guardandolo en una variable
        a_file = open(config_path, "r")
        json_cofig = json.load(a_file)
        a_file.close()

        string_to_execute = 'json_cofig'
        for i in level:
            string_to_execute = string_to_execute + f'["{ i }"]'


        # Modificando el campo que queremos modificar
        exec(f"{ string_to_execute } = { value }")

        # Guardando la variable en el file de config
        a_file = open(config_path, "w")
        json.dump(json_cofig, a_file, indent=3)
        a_file.close()
        print(f"Succesful changed:\n{ string_to_execute } = { value }")
        return "success"
    
    except Exception as e:
        print(f"ERROR: Could´t change config value:\n{ e }")
        return str(e)

# Recibe el directorio de recordings y devuelve un json con la cantidad de recordings y cuantos universos tiene cada uno
def get_recordings_info(recordings_path: str):
    try:
        recordings_list = os.listdir(recordings_path)
        recordings_list.sort()

        recordings_dir = {}
        recordings_dir["info"] = "recording index: amount of universes"
        recordings_dir["content"] = {}
        for i, scene in enumerate(recordings_list):
            recordings_dir["content"][i] = len(os.listdir(recordings_path + '/' + scene))
        return recordings_dir
    
    except Exception as e:
        print(f"There was an error in get_recordings_info() \n{ e }")

# Obtener numero de argumentos de una funcion
def get_function_number_of_arguments(function):
    from inspect import signature
    sig = signature(function)
    params = sig.parameters 
    return(len(params))

# Conocer el estado del request ¿El request esta corriendo? 1 Recibe lista de estados, el url del request y el numero de argumentos del request
def request_is_running(status_list: list, request_url:str, arguments_number: int):
    url_without_params = request_url.rsplit('/', arguments_number)[0]
    # Si el url sin parametros esta en la lista, entonces esta corriendo
    if url_without_params in status_list:
        return True
    else:
        return False

# Cambiar el estado de la lista de reuests
def set_request_status(status_list: list, request_url:str, arguments_number: int, running: bool):
    url_without_params = request_url.rsplit('/', arguments_number)[0]
    if running == True:
        status_list.append(url_without_params)
    elif running == False and url_without_params in status_list:
        status_list.remove(url_without_params)
    return status_list

def test_wait():
    for i in range(10):
        print(i)
        time.sleep(1)

# Funcion que lee del config si seguimos grabando
def keep_recording(config_path: str):
    # Files de configuracion
    data = json.load(open(config_path))
    return data["record"]

