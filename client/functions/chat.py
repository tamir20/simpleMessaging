import requests
from classes.chat_message import Chat_Message

def send_message(name: str, id: int, msg: str) -> None:
    port = id # as the id of the user is actually his port

    chat_message = Chat_Message(msg=msg, sender=name)

    requests.post(
      f'http://127.0.0.1:{port}/chat',
      data = chat_message.model_dump_json()
   )
    
def handle_print_message(msg: Chat_Message) -> None:
    msg.print_chat()