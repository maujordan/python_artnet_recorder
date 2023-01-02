from stupidArtnet import StupidArtnetServer
import json
import os
from csv import writer
import sys
from utils.utils import *
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=False) # Errores en color


# Files and folders names
config_file_name = 'config.json'
states_file_name = "states.json" # ombre del archivo que guarda estados


# Funcion principal
    # Recibe el status list y lo regresa cuando acabe de correr
def record_artnet():
    
    # Crea las variables globales que se necesitan para operar
    get_globals()

    delete_directory(scene_path)
    
    check_if_scene_path_exists(scene_path)
    # Poniendo el estado de la grabacion en el config file en true
    change_json_file_value(level=["currently_rcording"], config_path=config_path, value=True) 

    # Creando callback functions para escribir en los CSV
    for i in range(config_universes):
        file_name = '{0:03}.csv'.format(i)
        exec(f"""
def callback_u{ i }(data):
    print('Recording universe { i }:')
    #print(data)
    save_in_csv(output_name= scene_path + '/' + '{ file_name }', list_to_append=data) # Guardamos en un csv
    return
        """)

    # Reiniciando archivos csv de grabacion
    for i in range(config_universes):
        file_name = '{0:03}.csv'.format(i)
        # Si el archivo existe lo borramos
        os.remove(scene_path + '/' + file_name) if os.path.exists(scene_path + '/' + file_name) else print(f"{ i } Archivo no existe todavía")

    # Creando servidor
    server = StupidArtnetServer()

    # Creando listeners para la cantidad de universos que hay en el config.json, por ahora maximo 16
    for i in range(config_universes):
        exec(f"""
u{ i }_listener = server.register_listener(universe={ i }, callback_function=callback_u{ i }) 
        """)

        
    
    go_on = True
    while go_on == True:
        try:
            go_on = get_json_file(states_path)["new_recording"]
        except:
            pass
        if go_on == False:
            print("\nParamos grabacion")
            server.delete_all_listener()
            change_json_file_value(level=["new_recording"], config_path=states_path, value=False) # Cambiando el estado de la grabacion a false
    # Limpiando el servidor cuando teminamos
    # Creando listeners para la cantidad de universos que hay en el config.json, por ahora maximo 16
    for i in range(config_universes):
        exec(f"server.delete_listener(u{ i }_listener)")
        exec(f"""del u{ i }_listener""")
        
    del server
    
    
    return
# END: Funcion principal



# Funcones secundarias
    # Si el path de la grabación no existe, lo creamos
def check_if_scene_path_exists(scene_path: str):
    get_globals()
    recording_path_exists = os.path.exists(scene_path) # verificando si el path existe
    if recording_path_exists == False:
        os.makedirs(scene_path)
        print(f"The new is created at: \n \t{ scene_path }")
    return

# Función para appendear una lista en un csv. Recibe el nombre del archivo a appendear y la lista a appendear
def save_in_csv(list_to_append, output_name = "out.csv"):
	# from csv import writer
	with open(output_name, 'a') as f_object:
		writer_object = writer(f_object)
		writer_object.writerow(list_to_append)
		f_object.close() # Cerramos file


def get_globals():
    """
    Crea las variables globales que se necesitan para operar
    """
    global config_file_name, states_file_name, dir_path, config_path, states_path, config_json, selected_scene, config_universes, scene_path

    

    # Paths
    dir_path = os.path.dirname(__file__)
    config_path = dir_path + '/' + config_file_name
    states_path = os.path.join(dir_path, states_file_name)

    # Objetos
    config_json = json.load(open(os.path.join(dir_path, config_file_name)))
    selected_scene = config_json['selected_scene'] # Escena a grabar
    config_universes = config_json["settings"]["universes"] # Obteniendo cantidad de universos
    scene_path = dir_path + f"/recordings/scene_{ selected_scene }" 

#record_artnet()
