from stupidArtnet import StupidArtnetServer
import json
import os
from csv import writer
import sys
from utils.utils import *
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=False) # Errores en color


# Files de configuracion
dirname = os.path.dirname(__file__)
config_file_name = 'config.json'
config_path = dirname + '/' + config_file_name
data = json.load(open(os.path.join(dirname, config_file_name)))
selected_scene = data['selected_scene'] # Escena a grabar
scene_path = dirname + f"/recordings/scene_{ selected_scene }" 
config_universes = data["settings"]["universes"] # Obteniendo cantidad de universos

# Si el path de la grabación no existe, lo creamos
def check_if_scene_path_exists(scene_path: str):
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


def record_artnet():

    check_if_scene_path_exists(scene_path)



    # Creando callback functions para escribir en los CSV
    for i in range(config_universes):
        file_name = '{0:03}.csv'.format(i)
        exec(f"""
def callback_u{ i }(data):
    print('universo { i }:')
    print(data)
    save_in_csv(output_name= scene_path + '/' + '{ file_name }', list_to_append=data) # Guardamos en un csv
    return
        """)

    # Reiniciando archivos csv de grabacion
    for i in range(config_universes):
        file_name = '{0:03}.csv'.format(i)
        # Si el archivo existe lo borramos
        os.remove(scene_path + '/' + file_name) if os.path.exists(scene_path + '/' + file_name) else print("Archivo no existe todavía")

    # Creando servidor
    server = StupidArtnetServer()

    # Creando listeners para la cantidad de universos que hay en el config.json, por ahora maximo 16
    for i in range(config_universes):
        exec(f"""
u{ i }_listener = server.register_listener(universe={ i }, callback_function=callback_u{ i })
        """)

    
    
    change_congig_file_value(level=["record"], config_path=config_path, value=True) # Poniendo recording en true en config_file
    go_on = True
    while go_on == True:
        go_on = keep_recording(config_path=config_path)
        if go_on == False:
            print("\nParamos grabacion")
            server.delete_all_listener()
    del server
    
    return

# record_artnet()