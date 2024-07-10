import requests
from classes.chat_message import Chat_Message
from config.config import config_file
from functions.url_generator import get_chat_url_api
from enums.chat_api_enum import Chat_API_Enum

def send_message(name: str, id: int, msg: str) -> None:
    port = id # as the id of the user is actually his port

    chat_message = Chat_Message(msg=msg, sender=name)

    requests.post(
      get_chat_url_api(Chat_API_Enum.CHAT, port),
      data = chat_message.model_dump_json()
   )
    
def handle_print_message(msg: Chat_Message) -> None:
    msg.print_chat()