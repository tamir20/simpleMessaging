import threading
from fastapi import FastAPI
from functions.heartbeat import handle_send_heartbeat, app_port
from functions.client_app import get_port_not_in_use, handle_client_app, handle_input
from fastapi_utils.tasks import repeat_every


# Global variable that mantain client's connections
online_users = set()
app = FastAPI()

# @app.post("/heartbeat/")
# async def heartbeat(heartbeat: Heartbeat_Message) -> None:
#     handle_heartbeat(online_users, heartbeat)

# @app.get("/list/")
# async def list_online_users() -> set:
#     return handle_list_online_users(online_users)

@app.on_event('startup')
@repeat_every(seconds=1)  # Adjust the interval as needed
async def validate_online_users():
    handle_send_heartbeat()

if __name__ == "__main__":
    app_port[0] = get_port_not_in_use()
    threading.Thread(target=handle_client_app, args=[app, app_port[0]]).start()

    print('Enter Name:')
    name = input()
    print(f'welcome {name}')
    print('please state your destination id using "id <id>". to see available ids please use "list". see your name using "name"')
    while True:
        msg = input()
        if msg == "quit":
            break
        else:
            handle_input(msg, name, app_port[0])