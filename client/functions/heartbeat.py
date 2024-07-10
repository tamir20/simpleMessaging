import requests
from classes.heartbeat_message import *
from enums.server_api_enum import Server_API_Enum
from functions.url_generator import get_server_url_api

# the port of the applicaiton to hertbeat to the server
app_port = [0]
app_name = [""]

def handle_send_heartbeat() -> None:
   # print(f'sending heartbeat for name a and port {app_port[0]}')
   heartbeat = Heartbeat_Message(name=app_name[0], port=app_port[0])
   requests.post(
      get_server_url_api(Server_API_Enum.HEARTBEAT),
      data = heartbeat.model_dump_json()
   )
