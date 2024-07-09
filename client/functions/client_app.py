import socket
import requests
import uvicorn
from fastapi import FastAPI
import re
from classes.heartbeat_message import Heartbeat_Message
from functions.json_parser import convert_json_to_user_set

def get_user_list() -> int:
    response = requests.get('http://127.0.0.1:12000/list')
    user_set = convert_json_to_user_set(response.text)

    print(f"{'Name':10} {'ID'}")
    print(f"----------------\n")

    for user in user_set:
        print(f"{user.name:10} {user.port}\n")

def get_port_not_in_use() -> int:
    for port in range(12000,13001):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)):
                return port
            
def handle_client_app(app: FastAPI, port: int) -> None:
   uvicorn.run(app, host="127.0.0.1", port=port, log_level="critical", access_log=False, log_config=None)  # Specify the desired port here

def handle_input(msg: str, name: str, port: int) -> None:
    pattern = re.compile(r"^id \d+$")

    if msg == 'list':
        get_user_list()
    elif msg == 'name':
        print(name)
    elif not pattern.match(msg):
        print('please state your destination id using "id <id>". to see available ids please use "list". see your name using "name"')
    # else:
    #     handle_message()