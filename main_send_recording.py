import csv
from stupidArtnet import StupidArtnet
import time
import glob
import os
import json
import sys
from IPython.core import ultratb 
sys.excepthook = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=False) # Errores en color

start_time = time.time()

# Files de configuracion
path = os.path.dirname(__file__) # Path en el que estamos
recordings_path = path + '/recordings' # Path donde se encuentran los recordings
data = json.load(open(os.path.join(path, 'config.json')))
config_universes = data["settings"]["universes"] # Obteniendo cantidad de universos

# Valores necesarios para mandar artner
target_ip = data["settings"]["ip_address"]  # IP a la que enviaremos
packet_size = 512           # Tamaño del packet
framerate  = 30            # Framerate
#recordings_path = '/home/maurojordan/Documents/ws2812-over-artnet/recordings/' # Path donde se guardan los recordings

# Fucion para leer el csv que contiene la grabacion. Recibe el path al CSV y regresa la grabacion en forma de lista de listas
def read_recording(path: str):
    with open(path, newline='') as f:
        reader = csv.reader(f)
        list_recording = list(reader)

    return list_recording

# Funcion para obtener numero minimo de packets entre todos los universos creados
def min_recording_len(config_universes):
    list_len = []
    for i in range(config_universes):
        exec(f"len_{ i } = len(recording{ i })")
        exec(f"list_len.append(len_{ i })")
    
    return min(list_len)



############## Broadcasting recording

# Creando artnet_objects y CSVs de recordings
for i in range(config_universes):
    exec(f"artnet_object{ i } = StupidArtnet(target_ip, { i }, packet_size, framerate, True, True)") # Creando artnet objects
    exec(f"print(artnet_object{ i })")
    exec(f"artnet_object{ i }.start()") # Inicializando artnet objects para que reciban artnet


# Leyendo artnet recordings
list_recording_names = glob.glob(recordings_path + '/' +'/*.csv') # Obteniendo los nombres de los archivos .csv
list_recording_names.sort() # Ordenando alfabeticamente
for i, file_path in enumerate(list_recording_names): # For para leer todos los archivos CSV de la carpeta recordings
    if i == config_universes:
        break
    exec(f"recording{ i } = read_recording('{ file_path }')")
    print(f"Got recording { i }!")



# Obteniendo grabación con menor cantidadd de packets
min_packets = min_recording_len(config_universes)

print("Broadcastings...")
# Cargamos cada frame en cada uno de los universos
for i in range(min_packets):
    for j in range(config_universes):
        exec(f"artnet_object{ j }.set(list(map(int, recording{ j }[{ i }])))")
    time.sleep(1/framerate) # 30 HZ

# Mandando a 0 todos los canales
# Cargamos cada frame en cada uno de los universos
print("Sending 0 to all channels")
for i in range(config_universes):
    exec(f"artnet_object{ i }.blackout()")    

end_time = time.time()
print(f"Done!!! Execution time: { round((end_time - start_time)/60, 1) } minutes")

