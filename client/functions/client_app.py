import re
import socket
import logging
import uvicorn
import threading
from fastapi import FastAPI
from config.config import config_file
from functions.chat import send_message
from functions.print import print_user_list
from enums.chat_commands_enum import Chat_Commands_Enum
from labels.labels import ASK_USER_FOR_NAME, GENERAL_HELP, ID_SET_MESSAGE

def start_chat_api(app: FastAPI, port: int) -> None:
    threading.Thread(target=handle_client_app, args=[app, port]).start()

def start_chat_terminal(name: str) -> None:
    while True:
        msg = input()
        id = handle_input(msg, name, current_id)
        if id:
            current_id = id

def ask_user_name() -> str:
    print(ASK_USER_FOR_NAME)
    return input()

def get_port_not_in_use() -> int:
    for port in range(config_file["client"]["minimum_port"],config_file["client"]["maximum_port"]):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex((config_file["client"]["ip"], port)):
                return port
            
def handle_client_app(app: FastAPI, port: int) -> None:
   # run the fastapi app
   uvicorn.run(app, host=config_file["client"]["ip"], port=port, log_level=logging.CRITICAL, access_log=False, log_config=None)

def handle_id(msg: str) -> int:
    # i assume that the message has passed the regex inspection of 'id <number>'
    return int(msg.split()[1])

def handle_input(msg: str, name: str, id: int) -> int | None:
    pattern = re.compile(config_file["messages"]["id_message_regex_format"])
    updated_id = None # updated_id logic means that it will change target
    # id if the answer from this function is not 0

    if msg == Chat_Commands_Enum.LIST:
        print_user_list()
    elif msg == Chat_Commands_Enum.NAME:
        print(name)
    elif pattern.match(msg):
        updated_id = handle_id(msg)
        print(ID_SET_MESSAGE + str(updated_id))
    elif not id or msg == Chat_Commands_Enum.HELP:
        print(GENERAL_HELP)
    else:
        send_message(name, id, msg)

    return updated_id
    