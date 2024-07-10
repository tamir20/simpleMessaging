import re
import socket
import uvicorn
import requests
from fastapi import FastAPI
from functions.chat import send_message
from functions.json_parser import convert_json_to_user_set

def print_user_list() -> None:
    response = requests.get('http://127.0.0.1:12000/list')
    user_set = convert_json_to_user_set(response.text)

    print(f"{'Name':10} {'ID'}")
    print(f"----------------")

    for user in user_set:
        print(f"{user.name:10} {user.port}")

def get_port_not_in_use() -> int:
    for port in range(12000,13001):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)):
                return port
            
def handle_client_app(app: FastAPI, port: int) -> None:
   uvicorn.run(app, host="127.0.0.1", port=port, log_level="critical", access_log=False, log_config=None)  # Specify the desired port here

def handle_id(msg: str) -> int:
    return int(msg.split()[1])

def handle_input(msg: str, name: str, port: int, id: int) -> int:
    pattern = re.compile(r"^id \d+$")
    updated_id = 0

    if msg == 'list':
        print_user_list()
    elif msg == 'name':
        print(name)
    elif msg == 'help':
        print('please state your destination id using "id <id>". to see available ids please use "list". see your name using "name"')
    elif pattern.match(msg):
        updated_id = handle_id(msg)
        print(f'current id is set to {updated_id}')
    elif id:
        send_message(name, id, msg)
    else:
        print('please state your destination id using "id <id>". to see available ids please use "list". see your name using "name"')

    return updated_id
    