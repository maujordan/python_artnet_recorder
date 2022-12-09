from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import inspect
# User functions
from main_send_recording import broadcast_recording
from main_record_artnet import record_artnet
from utils.utils import *

# Parameters
scene_to_update = "scene_0"
text_to_place= "here goes some text"
# END  Parameters


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

update_description_file("scene_1")