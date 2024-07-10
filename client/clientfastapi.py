from fastapi import FastAPI
from config.config import config_file
from fastapi_utils.tasks import repeat_every
from classes.chat_message import Chat_Message
from functions.chat import handle_print_message
from functions.print import print_welcome_messsage
from functions.heartbeat import handle_send_heartbeat, app_port, app_name
from functions.client_app import get_port_not_in_use, ask_user_name, start_chat_terminal, start_chat_api


# Global variable that mantain client's connections
online_users = set()
app = FastAPI()

@app.post(config_file["client"]["api"]["chat"])
async def print_message(msg: Chat_Message) -> None:
    handle_print_message(msg)

@app.on_event('startup')
@repeat_every(seconds=1)  # Adjust the interval as needed
async def validate_online_users():
    handle_send_heartbeat()

if __name__ == "__main__":
    app_name[0] = ask_user_name()
    app_port[0] = get_port_not_in_use()
    print_welcome_messsage(app_name[0])
    start_chat_api(app, app_port[0])
    start_chat_terminal(app_name[0])
