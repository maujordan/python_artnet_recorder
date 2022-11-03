import RPi.GPIO as GPIO
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import json
import main_send_recording

# Nombre del directorio en el que estamos trabajando
dirname = os.path.dirname(__file__) + "/"

# Recordings path name
recordings_path_name = "/recordings"


# Obteniendo ip
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

host_name = get_ip()  # IP Address of Raspberry Pi
host_port = 8000

# Funcion para cambiar algun valor del config.json
def change_congig_file_value(level:list, value):
    try:
        # Obteniendo nombre de directorio
        config_file_name = "config.json"

        # Leyendo config file y guardandolo en una variable
        a_file = open(dirname + config_file_name, "r")
        json_cofig = json.load(a_file)
        a_file.close()

        string_to_execute = 'json_cofig'
        for i in level:
            string_to_execute = string_to_execute + f'["{ i }"]'


        # Modificando el campo que queremos modificar
        exec(f"{ string_to_execute } = { value }")

        # Guardando la variable en el file de config
        a_file = open(dirname + config_file_name, "w")
        json.dump(json_cofig, a_file, indent=3)
        a_file.close()
        print(f"Succesful changed:\n{ string_to_execute } = { value }")
        return "success"
    except Exception as e:
        print(f"ERROR: Could´t change config value:\n{ e }")
        exit()

#Fucion para crear la cantidad de botones de acuerdo a la cantidad de recordings que hay
def create_recordings_buttons():
    dir = os.path.dirname(__file__) + "/recordings" # Path en el que estamos
    num_recordings = len(os.listdir(dir)) # cantidad de archivos dentro del recording_path
    html_block = ''
    for i in range(num_recordings):
        html_block = html_block + f'<input type="submit" name="play_recording" value="{ i }"> \n'
    return html_block





class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        recording_buttons = create_recordings_buttons()
        html = \
        f'''
           <html>
           <body 
            style="width:960px; margin: 20px auto;">
           <h1>Access recordings</h1>
           <p>Here you can play the different recordings </p>
           <form action="/" method="POST">
               Play recording:
               { recording_buttons }
           </form>
           </body>
           </html>
        '''

        self.do_HEAD()
        self.wfile.write(html.encode("utf-8"))

    
    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = post_data.split("=")

        # Codigo para reproducir una grabación
        if post_data[0] == 'play_recording':
            
            selected_scene = post_data[1]
            # Ajustamos numero de universos a reproducir en el config file
                # Revisamos cuantos universos hay grabados en la escena
            scene_directory = dirname + recordings_path_name + f"/scene_{ selected_scene }"
            lst = os.listdir(scene_directory) # your directory path
            number_universes_in_scene = len(lst)
                # Cambiamos el config file a la cantidad de universos
            change_congig_file_value(["settings", "universes"], number_universes_in_scene)


            # Cambiamos la escena a reproducir en el config file
            change_congig_file_value(["selected_scene"], int(selected_scene)) # Cambiando config file
            main_send_recording.run() # Corriendo script
            

        self._redirect('/')  # Redirect back to the root url


# # # # # Main # # # # #

if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()