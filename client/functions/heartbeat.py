import uvicorn
import datetime
import requests
from fastapi import FastAPI
from classes.heartbeat_message import *
# from clientfastapi import app_port

# the port of the applicaiton to hertbeat to the server
app_port = [0]
app_name = [""]

def handle_send_heartbeat() -> None:
   # print(f'sending heartbeat for name a and port {app_port[0]}')
   heartbeat = Heartbeat_Message(name=app_name[0], port=app_port[0])
   requests.post(
      'http://127.0.0.1:12000/heartbeat',
      data = heartbeat.model_dump_json()
   )
