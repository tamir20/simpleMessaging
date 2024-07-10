import threading
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from classes.chat_message import Chat_Message
from functions.chat import handle_print_message
from functions.heartbeat import handle_send_heartbeat, app_port, app_name
from functions.client_app import get_port_not_in_use, handle_client_app, handle_input


# Global variable that mantain client's connections
online_users = set()
app = FastAPI()

@app.post("/chat")
async def print_message(msg: Chat_Message) -> None:
    handle_print_message(msg)

@app.on_event('startup')
@repeat_every(seconds=1)  # Adjust the interval as needed
async def validate_online_users():
    handle_send_heartbeat()

if __name__ == "__main__":
    current_id = 0

    print('Enter Name:')
    app_name[0] = input()

    app_port[0] = get_port_not_in_use()
    threading.Thread(target=handle_client_app, args=[app, app_port[0]]).start()

    print(f'welcome {app_name[0]}')
    print('please state your destination id using "id <id>". to see available ids please use "list". see your name using "name"')
    while True:
        msg = input()
        if msg == "quit":
            break
        else:
            id = handle_input(msg, app_name[0], app_port[0], current_id)
            if id:
                current_id = id