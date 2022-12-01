import csv
from stupidArtnet import StupidArtnet
import time
import glob
import os
import json
import sys
from utils.utils import *
from IPython.core import ultratb    
sys.excepthook = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=False) # Errores en color



def broadcast_recording(function_name, states_path):

    try:
        start_time = time.time()
        # Files de configuracion
        dir = os.path.dirname(__file__) # Path en el que estamos
        data = json.load(open(os.path.join(dir, 'config.json')))
        selected_scene = data['selected_scene'] # Escena a reproducir
        recordings_path = dir + f"/recordings/scene_{ selected_scene }"  # Path donde se encuentran los recordings

        # Obteniendo la cantidad de universos que vamos a lanzar 
        config_universes = len(os.listdir(recordings_path)) # cantidad de archivos dentro del recording_path
        if config_universes == 0:
            print("No recordings in this path")
            return

        # Valores necesarios para mandar artner
        target_ip = data["settings"]["ip_address"]  # IP a la que enviaremos
        packet_size = 512           # Tamaño del packet
        framerate  = 30            # Framerate
        #recordings_path = '/home/maurojordan/Documents/ws2812-over-artnet/recordings/' # Path donde se guardan los recordings

        # Fucion para leer el csv que contiene la grabacion. Recibe el dir al CSV y regresa la grabacion en forma de lista de listas
        def read_recording(dir: str):
            with open(dir, newline='') as f:
                reader = csv.reader(f)
                list_recording = list(reader)

            return list_recording

        # Funcion para obtener numero minimo de packets entre todos los universos creados
        def min_recording_len(recordings_list):
            list_len = []
            for rec in recordings_list:
                list_len.append(len(rec))
            
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
        recordings_list = []
        for i, file_path in enumerate(list_recording_names): # For para leer todos los archivos CSV de la carpeta recordings
            if i == config_universes:
                break
            temp_var =  read_recording(f'{ file_path }')
            exec(f"recording{ i } = temp_var") 
            exec(f"recordings_list.append(recording{ i })")
            print(f"Got recording for univers: { i }!")



        # Obteniendo grabación con menor cantidadd de packets
        #min_packets = min_recording_len(config_universes)
        min_packets = min_recording_len(recordings_list)
        del recordings_list # Eliminando variable para liberar espacio

        print("Broadcastings...")
        # Cargamos cada frame en cada uno de los universos
        read_recording_state = True
        while True:
            if read_recording_state  == False:
                    break
            for i in range(min_packets):
                # Leemos el estado de la grabacion antes de entrar en el loop
                try:
                    read_recording_state = get_json_file(states_path)["read_recording"]
                    pass
                except:
                    pass
                for j in range(config_universes):
                    exec(f"artnet_object{ j }.set(list(map(int, recording{ j }[{ i }])))")  
                # Si el estado de la grabación esta en false, paramos la grabacion
                if read_recording_state  == False:
                    print("Stopping broadcast...")
                    break
                print(f"Frame: { i }/{ min_packets }", end='\r')
                time.sleep(1/framerate) # 30 HZ

        # Mandando a 0 todos los canales
        # Cargamos cada frame en cada uno de los universos
        print("Sending 0 to all channels")
        for i in range(config_universes):
            exec(f"artnet_object{ i }.blackout()")    

        end_time = time.time()
        print(f"Done!!! Execution time: { round((end_time - start_time)/60, 1) } minutes")
    except Exception as e:
        print("There was an error when trying to play the recording:\n", e)
        change_json_file_value([function_name], states_path, False) # Cambiando estado de reproducción
        exit()
    
    change_json_file_value([function_name], states_path, False) # Cambiando estado de reproducción
    return