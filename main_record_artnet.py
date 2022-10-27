from stupidArtnet import StupidArtnetServer
import json
import os
from csv import writer
import sys
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=False) # Errores en color


# Files de configuracion
dirname = os.path.dirname(__file__)
data = json.load(open(os.path.join(dirname, 'config.json')))
selected_scene = data['selected_scene'] # Escena a grabar
recordings_path = dirname + f"/recordings/scene_{ selected_scene }" 
config_universes = data["settings"]["universes"] # Obteniendo cantidad de universos

# Si el path de la grabación no existe, lo creamos
recording_path_exists = os.path.exists(recordings_path) # verificando si el path existe
if recording_path_exists == False:
    os.makedirs(recordings_path)
    print(f"The new is created at: \n \t{ recordings_path }")

# Función para appendear una lista en un csv. Recibe el nombre del archivo a appendear y la lista a appendear
def save_in_csv(list_to_append, output_name = "out.csv"):
	# from csv import writer
	with open(output_name, 'a') as f_object:
		writer_object = writer(f_object)
		writer_object.writerow(list_to_append)
		f_object.close() # Cerramos file

# Creando callback functions para escribir en los CSV
for i in range(config_universes):
    file_name = '{0:03}.csv'.format(i)
    exec(f"""
def callback_u{ i }(data):
    print('universo { i }:')
    print(data)
    save_in_csv(output_name= recordings_path + '/' + '{ file_name }', list_to_append=data) # Guardamos en un csv
    return
    """)

# Reiniciando archivos csv de grabacion
for i in range(config_universes):
    file_name = '{0:03}.csv'.format(i)
    # Si el archivo existe lo borramos
    os.remove(recordings_path + '/' + file_name) if os.path.exists(recordings_path + '/' + file_name) else print("Archivo no existe todavía")

# Creando servidor
server = StupidArtnetServer()

# Creando listeners para la cantidad de universos que hay en el config.json, por ahora maximo 16
for i in range(config_universes):
    exec(f"""
u{ i }_listener = server.register_listener(universe={ i }, callback_function=callback_u{ i })
    """)

input("stop???")
del server