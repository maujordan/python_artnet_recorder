import os
import json
import time
import shutil
import os
import re
import shutil


# Funcion para cambiar algun valor del config.json
    # Recibe: elemento que vamos a cambiar en una lista, el config file path y el valor que vamos que insertaremos
def change_json_file_value(level:list, config_path:str, value):
    """
    Changes value from a .json file
    """
    try:
        # Leyendo config file y guardandolo en una variable
        a_file = open(config_path, "r")
        json_cofig = json.load(a_file)
        a_file.close()

        string_to_execute = 'json_cofig'
        for i in level:
            string_to_execute = string_to_execute + f'["{ i }"]'

        # Modificando el campo que queremos modificar
        if isinstance(value, str): #Si value es string se ponen comillas, si no, solo se pone value
            exec(f"{ string_to_execute } = '{ value }'")
        else:
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

def get_recordings_info(recordings_path: str, descriptions_path=None):
    """
    Gets information about the scenes recorded.
    If the descriptions path is given will return a dictonary with the descriptions if they exist
    """
    try:
        recordings_list = os.listdir(recordings_path)
        recordings_list.sort()

        recordings_dir = {}
        recordings_dir["info"] = "recording index: amount of universes"
        recordings_dir["content"] = {}
        for scene in recordings_list:
            scene_number = re.findall(r'\d+', scene)[0] # Obteniendo numero de escena
            recordings_dir["content"][scene_number] = len(os.listdir(recordings_path + '/' + scene)) # Obteniendo cantidad de universos

        # Obteniendo descripciones
        recordings_dir["descriptions"] = {}
        if descriptions_path != None:
            for scene in recordings_list:
                scene_number = re.findall(r'\d+', scene)[0] # Obteniendo numero de escena
                recordings_dir["descriptions"][scene_number] = get_recording_description(scene)
        else:
            recordings_dir["descriptions"] = None
        return recordings_dir
    
    except Exception as e:
        print(f"There was an error in get_recordings_info() \n{ e }")


"""
def get_recordings_info(recordings_path: str):
    
    Returns the following info about recordings:
    #- scene number
    #- ammount of universes
    #- description stored in "descriptions.json"
    
    try:
        recordings_list = os.listdir(recordings_path)
        recordings_list.sort()

        recordings_dir = {}
        recordings_dir["content"] = {}
        for i, scene in enumerate(recordings_list):
            scene_number = re.findall(r'\d+', scene)[0]
            recordings_dir["content"][scene_number] = {
                "universes": len(os.listdir(recordings_path + '/' + scene)),
                "description": get_recording_description(scene)
            }
        return recordings_dir
    
    except Exception as e:
        print(f"There was an error in get_recordings_info() \n{ e }")
"""





# Obtener numero de argumentos de una funcion
def get_function_number_of_arguments(function):
    from inspect import signature
    sig = signature(function)
    params = sig.parameters 
    return(len(params))

# Conocer el estado del request ¿El request esta corriendo? 1 Recibe lista de estados, el url del request y el numero de argumentos del request
def request_is_running(status_list: list, function_name: str):
    # Si el url sin parametros esta en la lista, entonces esta corriendo
    if function_name in status_list:
        return True
    else:
        return False

# Cambiar el estado de la lista de reuests
def set_request_status(status_list: list, function_name:str, running: bool):
    if running == True:
        status_list.append(function_name)
    elif running == False and function_name in status_list:
        status_list.remove(function_name)
    return status_list

async def test_wait():
    for i in range(10):
        print(i)
        await time.sleep(1)

# Funcion que lee del config si seguimos grabando
def keep_recording(config_path: str):
    # Files de configuracion
    data = json.load(open(config_path))
    return data["record"]

# Obtiene el config_file
def get_json_file(path):
    json_file = json.load(open(path)) # Config json
    return json_file

def get_number_of_universes_in_recording(recordings_path):
    """
    Gets de umber of universes in the recording path
    """
    number_of_universes = len(os.listdir(recordings_path))
    return number_of_universes


def find_devices_on_network():
    """
    Looks for devices in network running an "arp -a" command
    Returns: dict with {ip: mac}
    """

    import os
    import re

    # Corriendo arp -a desde python para encontrar dispositivos en la red
    devices = []
    for device in os.popen('arp -a'):
        devices.append(device)

    ips = []
    macs = []
    for device in devices:
        # Finding ip address in string
        ip_address = re.findall( r'[0-9]+(?:\.[0-9]+){3}', device )
        # Finding mac address in string
        p = re.compile(r'(?:[0-9a-fA-F]:?){12}')
        mac_address = re.findall(p, device)
        
        current_ip = ''
        if len(ip_address) > 0:
            current_ip = ip_address[0]
        else:
            current_ip = "No ip address for device"

        current_mac = ''
        if len(mac_address) > 0:
            current_mac = mac_address[0]
        else:
            current_mac = "No mac address for device"
        
        ips.append(current_ip)
        macs.append(current_mac)

    # Poniendo las ips y mac en un diccionario
    devices_dict = {}
    for i in range(len(ips)):
        devices_dict[ips[i]] = macs[i]


    return devices_dict

def delete_scene(recordings_path, scene_to_delete_string):
    """
    Deletes scene. It deletes the folder of the scene with all it´s contente
    Receives:
    - recordings_path: path to the recording folder
    - scene_to_delete_string: the scene that we are deleting. Example: "scene_2"
    """

    scene_to_delete_path = os.path.join(recordings_path, scene_to_delete_string)
    if os.path.exists(scene_to_delete_path) and os.path.isdir(scene_to_delete_path):
        shutil.rmtree(scene_to_delete_path)
        return 1
    else:
        print(f"Couldn´t delete { scene_to_delete_path } because it doesn´t exist.")
        return 0

    return 0

def get_ip_address():
    """
    Gets the device ip address
    """
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    direccion_ip = s.getsockname()[0]
    s.close()

    return direccion_ip


def update_description_file(scene_to_update, text_to_place="Here goes some description"):
    """
    Updatea el file de descripciones de escenas
    """
    # Check if scene exists
    with open("descriptions.json", "r") as jsonFile:
        descriptions_json = json.load(jsonFile)

    descriptions_json["descriptions"][scene_to_update] = text_to_place

    with open("descriptions.json", "w") as jsonFile:
        json.dump(descriptions_json, jsonFile)
    
    return

def get_recording_description(scene_to_get):
    """
    Returns description of scene stored in "descriptions.json"
    If the description doesnt exist yet then it will return "No description yet."
    """
    # Check if scene exists
    with open("descriptions.json", "r") as jsonFile:
        descriptions_json = json.load(jsonFile)

    description = "No description yet." if scene_to_get not in descriptions_json["descriptions"] else descriptions_json["descriptions"][scene_to_get]
    
    return description

def delete_directory(dirpath):
    """
    Elimina un directorio recibiendo el path, solo si existe 
    """
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"{ dirpath } eliminado")
        shutil.rmtree(dirpath)
    return

def CreateWifiConfig(SSID, password):
    """
    Changes the wifi SSID and password. Before running the permissions of the file have to be changed have to be changed running: sudo chmod 777 /etc/wpa_supplicant/wpa_supplicant.conf.
    Parameters:
        - SSID
        - password
    Returns: null
    """
    #setting up file contents
    config_lines = [
        'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
        'update_config=1',
        'country=MX',
        '\n',
        'network={',
        '\tssid="{}"'.format(SSID),
        '\tpsk="{}"'.format(password),
        '}'
        ]
    config = '\n'.join(config_lines)
    
    #display additions
    print(config)
    
    #give access and writing. may have to do this manually beforehand
    os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")
    
    #writing to file
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
        wifi.write(config)
    
    #displaying success
    print("wifi config added")

    #reboot, which impliments changes
    os.popen("sudo reboot")

    return

def create_folder_if_it_doesnt_exist(path):
    """
    Checks if a given folder path exists, if it doesn´t exist it creats it, if it exsists it does nothing.
    """
    if os.path.exists(path):
        return
    else:
        try:
            os.makedirs(path)
            print(f"The directory {path} was created successfully.")
        except OSError:
            print(f"The directory {path} could not be created.")
    return