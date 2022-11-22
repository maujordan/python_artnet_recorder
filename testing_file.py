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
import json
from utils.utils import *


level = ["settings", "ip_address"]
config_path = "./config.json"
value = "192.168.1.65"
    
        




