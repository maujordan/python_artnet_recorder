------------------------ Inicializar servidor ------------------------
- Iniciar el API app via terminal: uvicorn app:recorder_app --reload
- Iniciar api visible en la red local: uvicorn app:recorder_app --reload --host 0.0.0.0


------------------------ Para virtual environments ------------------------
- CREAR VIRTUAL ENVIRONMENT: python -m venv <nombre del entorno que creamos>
- ACTIVAR ENV source <nombre del entorno que creamos>/bin/activate
- SELECCIONAR INTERPRETE: Desde VS code en la linea de comandos buscar "select python interpreter" seleccionar el que creamos

------------------------ Crear nuevos endpoints ------------------------
- Si es endpoint de back end se debe agregar el nombre de la funcion en states.json


------------------------ Cronear on reboot ------------------------
HOME=/home/maujordan
@reboot cd /home/maujordan/Documents/python_artnet_recorder/ && python /home/maujordan/Documents/python_artnet_recorder/app.py
